from django.db import models
from django.db.models import signals
from django.conf import settings
from django.utils.translation import ugettext, ugettext_lazy as _

from django.contrib.auth.models import User, Group 
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from permissions.models import Role

from flexi_auth.managers import RoleManager

ROLES_DICT = dict(settings.ROLES_LIST)

class PermissionBase(object):
    """
    Just a mix-in class for permission management.
    
    Permission-checking methods defined here all return ``True``,
    so if a permission-enabled model class (one inheriting from
    ``PermissionBase``) doesn't override any of them, every user 
    is automatically granted the corresponding permissions.
    """
    # TODO: improve docstring
    
    # Table-level CREATE permission    
    @classmethod
    def can_create(cls, user, **kwargs):
        return True

    # Row-level LIST permission
    def can_list(self, user, **kwargs):
        return True
    
    # Row-level VIEW permission
    def can_view(self, user, **kwargs):
        return True
    
    # Row-level EDIT permission
    def can_edit(self, user, **kwargs):
        return True
    
    # Row-level DELETE permission
    def can_delete(self, user, **kwargs):
        return True
    
    
class ParamByName(object):
    """
    Helper class used to setup a convenient access API for ``ParamRole``'s parameters.
    """

    def _get_param(self, param_role, name):
        """
        If this role has a "%s" parameter, return it; else return None
        """
        # TODO: if a parameter is not set, an exception should be raised 
        # Retrieve the value of parameter named ``name``; if it's not set, return ``None``
        # Duck typing
        try: 
            rv = param_role.param_set.get(name=name).value
        except Param.DoesNotExist:
            rv = None

        return rv

#    def set_param(self, param_role, name, value):
#
#        param_names = map(lambda x : x[0], Param.PARAM_CHOICES)
#
#        #Sanity check
#        if name in param_names:
#            # TODO: check also content type
#            param_role.param_set.add(Param(name=name, param=value))
#        else:
#            raise NameError(ugettext("Wrong param name %s. Allowed param names are %s") % (value, param_names))

    def contribute_to_class(self, cls, name):
        """
        Create a property to retrieve role parameters by name
        """

        p = property(
            lambda obj : self._get_param(obj, name), 
            None,
            None, 
            self._get_param.__doc__ % name
        )

        setattr(cls, name, p)

class Param(models.Model):
    """
    A trivial wrapper model class around a generic ``ForeignKey``; 
    used to create (parametric) roles with more than one parameter.  
    """

    name = models.CharField(max_length=20, choices=settings.PARAM_CHOICES)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    value = generic.GenericForeignKey(ct_field="content_type", fk_field="object_id")

    def __unicode__(self):
        return u"%s" % self.value
        #return u"%s: %s" % (self.name, self.value)

    def __repr__(self):
        return "<%s %s: %s>" % (self.__class__.__name__, self.name, self.value)
    
    class Meta:
        # forbid duplicated ``Param`` entries in the DB
        unique_together = ('name', 'content_type', 'object_id')

class ParamRole(models.Model):
    """
    A custom role model class inspired by ``django-permissions``'s ``Role`` model.
    
    The goal is to augment the base ``Role`` model (carrying only a ``name`` field attribute) 
    with additional information to make it *context-aware* (i.e. turning it into a
    *parametric* role).    
    """
    
    # the basic ``Role`` to which additional context info is added (binding it to parameters)
    role = models.ForeignKey(Role)
    # parameters describing the context attached to this role 
    param_set = models.ManyToManyField(Param)
    
    ## A simple API providing easier access to the parameters attached to this role.
    # Usage: to retrieve the value of parameter ``<param_name>`` from the parametric role
    # instance ``p_role``, just use ``p_role.<param_name>`` 
    # If ``p_role`` doesn't have a parameter ``<param_name>`` attached to it, 
    # a ``RoleParameterNotAllowed`` exception is raised. 
    
    # Since the set of allowed parameters is domain-specific 
    # (declared using the project-level ``PARAM_CHOICES`` setting),
    # the access API must be dynamically built; to this end, we leverage the  
    # ``contribute_to_class`` Django machinery.
                     
    # note that this access is read-only; parameter assignment is managed by the 
    #``register_parametric_role()`` factory function.
    
    # TOOD: use ``ParamByName()`` field-like object to implement the access API for parameters.
    
    objects = RoleManager()

    def __unicode__(self):
        param_str_list = ["%s" % s for s in self.params]
        return u"%(role)s for %(params)s" % { 'role' : ROLES_DICT[self.role.name], 'params':  ", ".join(param_str_list)}
    
    @property
    def params(self):
        return self.param_set.all()
    
    @property
    def param(self):
        """
        If this role has only one parameter, return it; else raise a ``MultipleObjectsReturned`` exception.
        
        This is just a convenience method, useful when dealing with simple parametric roles 
        depending only on one parameter (a common situation).    
        """
        
        params = self.params
        if len(params) > 1:
            raise Param.MultipleObjectsReturned("This parametric role has more than one parameter: %s" % params)
        return params[0]   
    
    @classmethod
    def get_role(cls, role_name, **params):
        """
        Return the (unique) parametric role matching criteria provided as input arguments.
        
        Exceptions 
        ==========
        * If no parametric role matches these criteria, raise ``ObjectDoesNotExist``.
        * If more than one parametric role match these criteria, raise ``MultipleObjectsReturned``.
        * If ``role_name`` is not a valid identifier for a role, raises ``RoleNotAllowed`` exception.
        * If ``params`` contains an invalid parameter name, raises ``RoleParameterNotAllowed`` exception.
        * If provided parameter names are valid, but one of them is assigned to a wrong type, 
          (based on domain constraints), raises  ``RoleParameterWrongSpecsProvided`` exception.
                  
        """
        
        qs = cls.objects.get_param_roles(role_name, **params)
        # TODO UNITTEST: write unit tests for this method
        if len(qs) > 1:
            raise cls.MultipleObjectsReturned("Warning: duplicate parametric role instances in the DB: %s with params %s" % role_name, params) 
        return qs[0]

    def add_principal(self, principal):
        """
        Add the given principal (user or group) to this parametric role.
        
        Raise a ``TypeError`` if the principal is neither a ``User`` nor a ``Group`` instance.
        """
        
        if isinstance(principal, User):
            #PrincipalParamRoleRelation.objects.create(user=principal, role=self)
            xobj, xcreated = PrincipalParamRoleRelation.objects.get_or_create(user=principal, role=self)
            #TODO LOG: whether add_principal is called and xreated = False. It should not happen...            
        elif isinstance(principal, Group):
            #PrincipalParamRoleRelation.objects.create(group=principal, role=self)
            xobj, xcreated = PrincipalParamRoleRelation.objects.get_or_create(group=principal, role=self)
            #TODO LOG: whether add_principal is called and xreated = False. It should not happen...
        else:
            raise TypeError("The principal must be either a User instance or a Group instance.")   

            
    def get_groups(self):
        """
        Returns all groups to which this parametric role is assigned.
        """
        
        qs = Group.objects.filter(principal_param_role_set__role=self)
        return qs    
        
    def get_users(self):
        """
        Returns all users to which this parametric role was assigned. 
        """
        
        qs = User.objects.filter(principal_param_role_set__role=self)
        return qs
    
    ##--------------- Archive API --------------##
    @property
    def is_active(self):
        """
        Return ``True`` if this parametric role is considered to be 'active'; ``False`` otherwise.
        
        What 'active' means may vary on a per-role basis; in general, a parametric role
        is considered to be 'active' iff **all** its parameters are active 
        (as model instances).
        
        In turn, to specify the relevant semantic for a model 
        (i.e. define when an instance of it is to be considered as 'active'),
        you need to implement an ``.is_active()`` instance method on the model class.                
        """
        
        # A role is active iff **all** its parameters are active
        is_active = True
        for p in self.params:
            # delegate the "activity" check to the parameter's model instance
            try:
                if not p.value.is_active():
                    is_active = False
                    break
            except NameError: 
                # Archive API is not implemented by that model, so assume that 
                # every instance is active by convention
                return True                
        return is_active             
    
    @property
    def is_archived(self):
        """
        Return ``True`` if this parametric role is considered to be 'archived'; ``False`` otherwise.
        
        What 'archived' means may vary on a per-role basis; in general, a parametric role
        is considered to be 'archived' iff **at least** one of its parameters is archived 
        (as a model instance).
        
        In turn, to specify the relevant semantic for a model 
        (i.e. define when an instance of it is to be considered as 'archived'),
        you need to implement an ``.is_archived()`` instance method on the model class.                
        """
        
        # This implementation assumes that 'active' and 'archived' are the only two  
        # allowed states for a parametric role, so they are mutually esclusive; 
        # if this assumption is invalid, a more general implementation may be needed 
        # (such as that of the ``.is_active()`` method above).   
        return not self.is_active()  
    
    ##---------------------------------------##

class PrincipalParamRoleRelation(models.Model):
    """
    This model is a relation describing the fact that a parametric role (``ParamRole``) 
    is assigned to a principal (i.e. a ``User`` or ``Group`` instance). 

    user
        The user to which the parametric role should be assigned. 
        Either a ``User`` instance xor a ``Group`` instance is needed here.

    group
        The group to which the parametric role should be assigned. 
        Either a ``User`` instance xor a ``Group`` instance needs is needed here.

    role
        The role (a ``ParamRole`` instance) to be assigned to the principal.
        
    CREDITS: this class is inspired by the ``PrincipalRoleRelation`` model in ``django-permissions``.
    """
    
    user = models.ForeignKey(User, blank=True, null=True, related_name="principal_param_role_set")
    group = models.ForeignKey(Group, blank=True, null=True, related_name="principal_param_role_set")
    role = models.ForeignKey(ParamRole, related_name="principal_param_role_set")

    def __unicode__(self):
        return _("%(user)s is %(role)s") % { 'user' : self.user, 'role' : self.role }

    def get_principal(self):
        """
        Returns the principal.
        """
        return self.user or self.group

    def set_principal(self, principal):
        """
        Sets the principal.
        """
        if isinstance(principal, User):
            self.user = principal
        elif isinstance(principal, Group):
            self.group = principal
        else:
            raise TypeError("The principal must be either a User instance or a Group instance.")

    principal = property(get_principal, set_principal)    
    
def setup_roles(sender, instance, created, **kwargs):
    """
    Setup any needed parametric role after a model instance is saved to the DB for the first time.
    This function just calls the ``.setup_roles()`` instance method of the sender model class (if defined);
    actual role-creation/setup logic is encapsulated there.
    """
    
    if created: # automatic role-setup should happen only at instance-creation time 
        try:
            # ``instance`` is the model instance that has just been created
            instance.setup_roles()
                                                
        except AttributeError:
            # sender model doesn't specify any role-related setup operations, so just ignore the signal
            pass

# add the ``setup_roles()`` function as a listener for the ``post_save`` signal
signals.post_save.connect(setup_roles)     
