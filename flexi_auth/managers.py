from django.db import models
from django.db.models import ObjectDoesNotExist
from django.contrib.contenttypes.models import ContentType
from django.conf import settings

from flexi_auth.exceptions import RoleNotAllowed, RoleParameterNotAllowed, RoleParameterWrongSpecsProvided
from flexi_auth.query import RoleQuerySet 

class RoleManager(models.Manager):
    """ 
    A custom Manager class for the ``ParamRole`` model.
    
    Useful for retrieving parametric roles based on role name and parameters
    (via the ``.get_param_roles()`` method).
    
    """
    
    def get_query_set(self):
        """
        Return a custom subclass of Django's standard ``QuerySet``, 
        augmented with methods useful for managing parametric roles.
        """
        return RoleQuerySet(self.model)
    
    def get_param_roles(self, role_name, **params):
        """
        This method retrieves the parametric roles satisfying the criteria provided as input.
        
        **Arguments**
        
        ``role_name``
            An identifier string matching one of the (non-parametric) roles allowed by 
            the application domain. 
        ``params``
            A dictionary of keyword arguments representing a pattern of parameters with respect to which 
            restricting the query.
            
        **Return Values**
        
        If input values are fine (with respect to the given application domain), ``.get_param_roles()``  returns
        the ``QuerySet`` of all ``ParamRole``s whose type is ``role_name`` and whose parameter set is a superset of ``params``.
        
        If ``role_name`` is not a valid identifier for a role, raises ``RoleNotAllowed`` exception.
        
        If ``params`` contains an invalid parameter name, raises ``RoleParameterNotAllowed`` exception.
        
        If provided parameter names are valid, but one of them is assigned to a wrong type,
        (based on domain constraints), raises  ``RoleParameterWrongSpecsProvided`` exception.
                  
        """
        
        from flexi_auth.utils import get_ctype_from_model_label
        
        # sanity checks
        try: 
            allowed_param_names = settings.VALID_PARAMS_FOR_ROLES[role_name].keys()
        except KeyError:
            raise RoleNotAllowed(role_name)
        for k in params.keys():
            if k not in allowed_param_names: 
                raise RoleParameterNotAllowed(role_name, allowed_param_names, k)
            expected_ctype = get_ctype_from_model_label(settings.VALID_PARAMS_FOR_ROLES[role_name][k])
            actual_ctype = ContentType.objects.get_for_model(params[k])
            if expected_ctype != actual_ctype:
                raise RoleParameterWrongSpecsProvided(role_name, params)                 
        
        pr_list = []
        # filter out parametric roles of the right type
        p_roles = self.get_query_set().filter(role__name__exact=role_name)
        # select only parametric roles whose parameters are compatible with those specified as input
        for pr in p_roles:
            # a flag used to exclude roles with a mis-matching parameter set 
            match = True
            for (k, v) in params.items():
                try:
                    #parameter name match, but value don't 
                    if not pr.param_set.get(name=k).value == v:
                        match = False
                # in case a parameter has a globally valid name, but not in this role's context
                except ObjectDoesNotExist:  
                    raise RoleParameterWrongSpecsProvided(role_name, params)
            # all tests were passed, so this parametric role matches with the query
            if match:
                pr_list.append(pr)
                
        qs = self.filter(pk__in=[obj.pk for obj in pr_list])
        return qs
   
   ##--------------- Archive API --------------##      
    def active(self, role_name, **params):
        """
        Return all **active** parametric roles satisfying the criteria provided as input.
        
        Signature and behaviour are the same as those of the ``.get_param_roles()`` method above.      
        
        """
        return self.get_param_roles(self, role_name, **params).active()
    
    def archived(self, role_name, **params):
        """
        Return all **archived** parametric roles satisfying the criteria provided as input.
        
        Signature and behaviour are the same as those of the ``.get_param_roles()`` method above.      
        
        """
        return self.get_param_roles(self, role_name, **params).archived()
    
    ##---------------------------------------##

