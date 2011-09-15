from django.test import TestCase
from django.contrib.auth.models import User, Group, AnonymousUser 
from django.contrib.contenttypes.models import ContentType

from flexi_auth.utils import get_ctype_from_model_label
from flexi_auth.exceptions import WrongPermissionCheck 
from flexi_auth.models import ObjectWithContext

from flexi_auth.tests.models import Article, Book, Author


class GetCtypeFromModelLabelTest(TestCase):
    """Tests for the ``get_ctype_from_model_label()`` function"""
    
    def setUp(self):
            pass
    
    def testOK(self):
        """Verify the right ContentType is returned if the model label is good"""
        user_ct = ContentType.objects.get_for_model(User)
        ct = get_ctype_from_model_label('auth.User')
        self.assertEqual(ct, user_ct)
        
    def testMalformedLabel(self):
        """Return None if the label is malformed"""        
        ct = get_ctype_from_model_label('auth:User')
        self.assertIsNone(ct)
        
    def testModelNotExisting(self):
        """Return None if the label points to a non existing model"""
        ct = get_ctype_from_model_label('auth.Foo')
        self.assertIsNone(ct)
        

class ParamByNameTest(TestCase):
    """Test if parameters of a parametric role can be accessed by name"""

    def setUp(self):
        pass
    
    def testGetOK(self):
        """Verify that an existing parameter can be retrieved by its name"""
        pass
    
    def testGetFailIfParameterNotSet(self):
        """When trying to retrieve an unset parameter, raise ``RoleParameterNotAllowed``"""
        pass


class ParamModelTest(TestCase):
    """Test behaviour of the ``Param`` model"""

    def setUp(self):
        pass
    
    def testParamUniqueness(self):
        """No duplicated ``Param``'s instances should exist in the DB"""
        pass

class ParamRoleAsDictTest(TestCase):
    """Tests for the ``parametric_role_as_dict()`` helper function"""
    
    def setUp(self):
        pass
    
    def testConversionOK(self):
        """If a ``ParamRole`` instance is passed, return a dictionary representing it"""
        pass
    
    def testConversionFail(self):
        """If the argument isn't a ``ParamRole`` instance, raise a ``TypeError``"""
        pass

        
class ParamRoleAsDictValidationTest(TestCase):
    """Tests for the ``_is_valid_parametric_role_dict_repr()`` helper function"""
    
    def setUp(self):
        pass
    
    def testValidationOK(self):
        """If a dictionary has the right structure to represent a parametric role, return ``True``"""
        pass
    
    def testValidationFailIfNotDict(self): 
        """If passed dictionary hasn't expected keys, return ``False``  """
        pass
    
    def testValidationFailIfNotRole(self): 
        """If ``role`` key is not a ``Role`` model instance, return ``False``"""

        pass

    def testValidationFailIfNotParams(self): 
        """If ``params`` key is not a dictionary, return ``False``"""
        pass

        
class ParamRoleComparisonTest(TestCase):
    """Tests for the ``_compare_parametric_roles()`` helper function"""
    
    def setUp(self):
        pass
    
    def testComparisonOK(self):
        """If arguments describe the same parametric role, return ``True``"""
        pass
    
    def testFailIfNotSameKind(self):
        """If arguments describe parametric roles of different kind, return ``False``"""
        pass
    
    def testFailIfNotSameParameters(self):
        """If arguments describe parametric roles with different parameters, return ``False``"""
        pass
    
    def testErrorIfTooManyArguments(self): 
        """If more than two arguments are given, raise ``TypeError``"""
        pass
    
    def testErrorIfNotEnoughArguments(self):
        """If less than two arguments are given, raise ``TypeError``"""
    
    def testErrorIfInvalidArguments(self):
        """If an argument is neither a ParamRole instance nor a valid dictionary representation for it, raise ``TypeError``"""

        
class ParamRoleValidationTest(TestCase):
    """Tests for the ``_validate_parametric_role`` function"""
    def setUp(self):
        pass
   
    def testValidationOK(self):
        """Verify that validation of a parametric role succeeds if arguments are fine"""
        pass
    
    def testValidationFailIfRoleNotAllowed(self):
        """Verify that validation of a parametric role fails if basic role isn't allowed"""
        pass
    
    def testValidationFailIfParamNameNotAllowed(self):
        """Verify that validation of a parametric role fails if a param's name isn't allowed"""
        pass
    
    def testValidationFailIfParamTypeNotAllowed(self):
        """Verify that validation of a parametric role fails if a param's type isn't allowed"""
        pass
    
    def testValidationOKIfNoConstraints(self):
        """Verify that validation of any parametric role succeeds if no costraints are specified"""
        pass

    
class ParamRoleRegistrationTest(TestCase):
    """Tests for the ``register_parametric_role`` function"""
    def setUp(self):
        pass
    
    def testRegistrationOK(self):
        """Verify that registration of a parametric role succeeds if arguments are fine"""
        pass
    
    def testRegistrationFailIfRoleNotAllowed(self):
        """Verify that registration of a parametric role fails if basic role isn't allowed"""
    pass

    def testRegistrationFailIfParamNameNotAllowed(self):
        """Verify that registration of a parametric role fails if a param's name isn't allowed"""
        pass
    
    def testRegistrationFailIfParamTypeNotAllowed(self):
        """Verify that registration of a parametric role fails if a param's type isn't allowed"""
        pass
    
    def testAvoidDuplicateParamRoles(self):
        """If a given parametric role already exists in the DB, don't duplicate it"""
        pass


class AddParametricRoleTest(TestCase):
    """Tests for the ``add_parametric_role`` function"""

    def setUp(self):
        pass

    def testAddToUserOK(self):
        """If a ``User`` instance is passed, the parametric role gets assigned to that user"""
        pass
    
    def testAddToUserRoleAlreadyAssigned(self):
        """If the role was already assigned to the user, return ``False``"""
        pass     
        
    def testAddToGroupOK(self):
        """If a ``Group`` instance is passed, the parametric role gets assigned to that group"""
        pass
    
    def testAddToGroupRoleAlreadyAssigned(self):
        """If the role was already assigned to the group, return ``False``"""
        pass           
        
    def testWrongPrincipalType(self):
        """If the principal is neither a ``User`` nor a ``Group`` instance, raise ``TypeError``"""
    
    
class RemoveParametricRoleTest(TestCase):
    """Tests for the ``remove_parametric_role()`` function"""

    def setUp(self):
        pass

    def testRemoveFromUserOK(self):
        """If a ``User`` instance is passed, the parametric role gets removed from that user"""
        pass
    
    def testRoleNotAssignedToUserBefore(self):
        """If the role wasn't already assigned to the user, return ``False``"""
        pass     
        
    def testRemoveFromGroupOK(self):
        """If a ``Group`` instance is passed, the parametric role gets removed from that group"""
        pass
    
    def testRoleNotAssignedToGroupBefore(self):
        """If the role wasn't already assigned to the group, return ``False``"""
        pass    
        
    def testWrongPrincipalType(self):
        """If the principal is neither a ``User`` nor a ``Group`` instance, raise ``TypeError``"""
        
class ClearParametricRolesTest(TestCase):
    """Tests for the ``clear_parametric_roles()`` function"""

    def setUp(self):
        pass

    def testRemoveFromUserOK(self):
        """If a ``User`` instance is passed, all parametric roles get removed from that user"""
        pass
    
    def testNoRoleAssignedToUserBefore(self):
        """If no role had been previously assigned to the user, return ``False``"""
        pass     
        
    def testRemoveFromGroupOK(self):
        """If a ``Group`` instance is passed, all parametric roles get removed from that group"""
        pass
    
    def testNoRoleAssignedToGroupBefore(self):
        """If no role had been previously assigned to the group, return ``False``"""
        pass    
        
    def testWrongPrincipalType(self):
        """If the principal is neither a ``User`` nor a ``Group`` instance, raise ``TypeError``"""


class GetParametricRolesTest(TestCase):
    """Tests for the ``get_parametric_roles()`` function"""

    def setUp(self):
        pass

    def testGetForUserOK(self):
        """If a ``User`` instance is given, retrieve all the parametric roles assigned to it"""
        pass
    
    def testGetForGroupOK(self):
        """If a ``Group`` instance is given, retrieve all the parametric roles assigned to it"""
        pass
        
    def testWrongPrincipalType(self):
        """If the principal is neither a ``User`` nor a ``Group`` instance, raise ``TypeError``"""


class GetAllParametricRolesTest(TestCase):
    """Tests for the ``get_all_parametric_roles()`` function"""

    def setUp(self):
        pass

    def testGetForUserOK(self):
        """If a ``User`` instance is given, retrieve all the parametric roles assigned to it, directly or via its groups"""
        pass
    
    def testGetForGroupOK(self):
        """If a ``Group`` instance is given, retrieve all the parametric roles assigned to it"""
        pass
        
    def testWrongPrincipalType(self):
        """If the principal is neither a ``User`` nor a ``Group`` instance, raise ``TypeError``"""

    
class RoleAutoSetupTest(TestCase):
    """Test automatic role-setup operations happening at instance-creation time"""

    def setUp(self):
        pass

class ParamRoleModelTest(TestCase):
    """Test basic behaviour of the ``ParamRole`` model"""

    def setUp(self):
        pass
    
    def testSingleParameterRetrieval(self):
        """Tests for the ``ParamRole.param()`` method"""
        pass


class ParamRoleGetRoleTest(TestCase):
    """Tests for``ParamRole.get_role()`` class method"""

    def setUp(self):
        pass
    
    def testGetRoleOK(self):
        """Check that ``ParamRole.get_role()`` behave as expected if passed arguments are fine"""
        pass
    
    def testNoMatchingRole(self):
        """If no parametric role matches input criteria, raise ``ObjectDoesNotExist``"""
        pass

    def testMultipleMatchingRole(self):
        """If more than one parametric role match input criteria, raise ``MultipleObjectsReturned``"""
        pass

    def testWrongRole(self):
        """If ``role_name`` is not a valid identifier for a role, raise ``RoleNotAllowed``"""
        pass

    def testWrongParamName(self):
        """If ``params`` contains an invalid parameter name, raise ``RoleParameterNotAllowed``"""
        pass

    def testWrongParamSpecification(self):
        """If a wrong param specification is given, raise ``RoleParameterWrongSpecsProvided``"""
        pass
  
  
class AddParamRoleToPrincipalTest(TestCase):
    """Tests for the ``ParamRole.add_principal()`` method"""

    def setUp(self):
        pass

    def testAddToUserOK(self):
        """Verify that if a ``User`` instance is passed, the parametric role gets assigned to that user"""
        pass
        
    def testAddToGroupOK(self):
        """Verify that if a ``Group`` instance is passed, the parametric role gets assigned to that group"""
        pass   
        
    def testAddFail(self):
        """If neither a ``User`` nor a ``Group`` instance is passed, raise ``TypeError``"""


class ParamRoleGetUsersTest(TestCase):
    """Tests for the ``ParamRole.get_users()`` method"""
    
    def setUp(self):
        pass
    
    def testGetUsersOK(self):
        """Verify that all the users this parametric role was assigned to are returned"""
        pass

    
class ParamRoleGetGroupsTest(TestCase):
    """Tests for the ``ParamRole.get_groups()`` method"""
    
    def setUp(self):
        pass
    
    def testGetGroupsOK(self):
        """Verify that all the groups this parametric role was assigned to are returned"""
        pass


class ParamRoleArchiveAPITest(TestCase):
    """Test the 'archive API' for ``ParamRole``s"""
    
    def setUp(self):
        pass
    
    def testIsActiveOK(self):
        """Check that ``ParamRole.is_active`` behaves as expected under normal conditions"""
        pass
    
    def testIsArchived(self):
        """Check that ``ParamRole.is_archived`` behaves as expected under normal conditions"""
        pass
    
    def testArchiveAPINotImplemented(self):
        """Check that ``ParamRole.is_(active|archived)`` behaves as expected if some parameter doesn't implement the 'archive API'"""
        pass

    
class PrincipalRoleRelationTest(TestCase):
    """Tests for the ``PrincipalRoleRelation`` model methods"""
    
    def setUp(self):
        pass
    
    def testGetPrincipalOK(self):
        """Test if the principal (user or group) is correctly retrieved"""
        pass
    
    def testSetPrincipalOK(self):
        """Test if the principal (user or group) is correctly set"""
        pass
        
    def testSetPrincipalError(self):
        """If neither a ``User`` nor a ``Group`` instance is passed, raise ``TypeError``"""
        pass
 
    
class RoleManagerTest(TestCase):
    """Tests for the ``RoleManager`` custom manager class"""

    def setUp(self):
        pass
    
    def testShallowCopyOk(self):
        """It should be possible to make a shallow copy of a manager instance"""
        # see https://docs.djangoproject.com/en/1.3/topics/db/managers/#implementation-concerns
        pass
    
    def testGetParamRolesOK(self):
        """Check that ``.get_param_roles()`` returns the right set of parametric roles if input is valid"""
        pass
    
    def testGetParamRolesFailIfInvalidRole(self):
        """If given an invalid role name, ``.get_param_roles()`` should raise ``RoleNotAllowed``"""
        pass
    
    def testGetParamRolesFailIfInvalidParamName(self):
        """If the name of parameter is invalid ``.get_param_roles()`` should raise ``RoleParameterNotAllowed``"""
        pass
    
    def testGetParamRolesFailIfInvalidParamType(self):
        """If the value of a parameter is of the wrong type, ``.get_param_roles()`` should raise RoleParameterWrongSpecsProvided"""
        pass
    
    def testArchiveAPIOK(self):
        """Check that ``.is_(active|archived)`` behaves as expected under normal conditions""" 
        pass
    
    def testArchiveAPINotImplemented(self):
        """Check that ``.is_(active|archived)`` behaves as expected if some parameter doesn't implement the 'archive API'"""
        pass
      
    def testArchiveAPIFailIfInvalidRole(self):
        """If given an invalid role name, ``.is_(active|archived)`` should raise ``RoleNotAllowed``"""
        pass
    
    def testArchiveAPIFailIfInvalidParamName(self):
        """If the name of parameter is invalid ``.is_(active|archived)`` should raise ``RoleParameterNotAllowed``"""
        pass
    
    def testArchiveAPIFailIfInvalidParamType(self):
        """If the value of a parameter is of the wrong type, ``.is_(active|archived)`` should raise RoleParameterWrongSpecsProvided"""
        pass 
       

class ParamRoleBackendTest(TestCase):
    """Tests for the ``ParamRoleBackend`` custom authorization backend"""

    def setUp(self):
        self.user = User.objects.create(username="Ian Solo")
        self.super_user = User.objects.create(username="Harry Potter", is_superuser=True)       
        self.anon_user = AnonymousUser()
        self.inactive_user = User.objects.create(username="Albus Silente", is_active=False)
        
        self.author1 = Author.objects.create(name="Bilbo", surname="Baggins")
        self.author2 = Author.objects.create(name="Luke", surname="Skywalker")
        
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author1)
        
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        self.book.authors.add(self.author1, self.author2)
        
    def _pack_context(self, model_or_instance, **context):
        """
        This helper method just packs a model class/instance and a context dictionary 
        into a single object ready to be passed to ``User.has_perm()``.
        """
        obj = ObjectWithContext(model_or_instance, context)        
        return obj
        
    def testSuperUsersCanDoEverything(self):
        """Test that superusers always pass permission checks"""
        user = self.super_user
        article = self.article
        book = self.book
        
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertTrue(user.has_perm('CREATE', obj))
        # Table-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article, website="FooSite") 
        self.assertTrue(user.has_perm('CREATE', obj))
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertTrue(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertTrue(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertTrue(user.has_perm('VIEW', obj))
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertTrue(user.has_perm('VIEW', obj))
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertTrue(user.has_perm('CREATE',obj))
        # Table-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book, language="Italian") 
        self.assertTrue(user.has_perm('CREATE', obj))
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertTrue(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertTrue(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertTrue(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertTrue(user.has_perm('VIEW', obj))     
    
    def testAnonymousUsersCanDoNothing(self):
        """Test that anonymous users always fail permission checks"""
        user = self.anon_user
        article = self.article
        book = self.book
        
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertFalse(user.has_perm('CREATE', obj))
        # Table-level permission, with context, model not subclassing  ``PermissionBase`` 
        obj = self._pack_context(Article, website="FooSite")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertFalse(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertFalse(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertFalse(user.has_perm('VIEW', obj))
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertFalse(user.has_perm('CREATE', obj))
        # Table-level permission, with context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertFalse(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertFalse(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertFalse(user.has_perm('VIEW', obj))  
    
    
    def testInactiveUsersCanDoNothing(self):
        """Test that inactive users always fail permission checks"""
        user = self.inactive_user
        article = self.article
        book = self.book
        
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertFalse(user.has_perm('CREATE', obj))
        # Table-level permission, with context, model not subclassing  ``PermissionBase`` 
        obj = self._pack_context(Article, website="FooSite")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertFalse(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertFalse(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertFalse(user.has_perm('VIEW', obj))
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertFalse(user.has_perm('CREATE', obj))
        # Table-level permission, with context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertFalse(user.has_perm('CREATE', obj))
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertFalse(user.has_perm('VIEW', obj))
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertFalse(user.has_perm('VIEW', obj))
    
    def testGlobalPermissionsDelegation(self):
        """If checking a non-object (global) permission, return ``False``"""
        user = self.user
        self.assertFalse(user.has_perm('add_user'))
           
        user = self.anon_user
        self.assertFalse(user.has_perm('add_user'))
        
        user = self.inactive_user
        self.assertFalse(user.has_perm('add_user'))
            
        
    def testWrongUserArgument(self):
        """If ``user_obj`` is not an ``User`` instance, raise ``AttributeError`` """
        # TODO
        pass
    
    def testWrongPermissionCheck(self):
        """If requesting a permission check not implemented by a model, raise ``WrongPermissionCheck`` """
        article = self.article
        book = self.book
        
        # "Regular" user
        user = self.user
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj) 
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        
        ## Superusers by-pass all access-control cheks, so there is no simple way
        ## to raise a ``WrongPermissionCheck`` when checking a "non-existent"
        ## permission (without patching Django !)        
        
        ## Inactive user
        user = self.inactive_user
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj) 
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj) 
        
        ## Anonymous user
        user = self.anon_user
        # Table-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj) 
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        
        # Table-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Table-level permission, with context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        obj = self._pack_context(Book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'CRATE', obj)
        # Row-level permission, no context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        # Row-level permission, with context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)
        obj = self._pack_context(book, language="Italian", cover="Paperback")
        self.assertRaises(WrongPermissionCheck, user.has_perm, 'MEW', obj)    
    
    
    def testTableLevelPermission(self):
        """Tests for table(class)-level permission-checking"""
        user = self.user
        
        # No context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(Article)
        self.assertFalse(user.has_perm('CREATE', obj))
        # With context, model not subclassing  ``PermissionBase`` 
        obj = self._pack_context(Article, website="FooSite")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Article, website="BarSite")
        self.assertTrue(user.has_perm('CREATE', obj))
        obj = self._pack_context(Article, website="FooSite", edition="morning")
        self.assertTrue(user.has_perm('CREATE', obj))
        
        # No context, model subclassing  ``PermissionBase``
        obj = self._pack_context(Book)
        self.assertFalse(user.has_perm('CREATE', obj))
        # With context, model subclassing  ``PermissionBase`` 
        obj = self._pack_context(Book, language="Italian")
        self.assertTrue(user.has_perm('CREATE', obj))
        obj = self._pack_context(Book, language="French")
        self.assertFalse(user.has_perm('CREATE', obj))
        obj = self._pack_context(Book, language="Dutch", cover="Paperback")
        self.assertTrue(user.has_perm('CREATE', obj))
        
    def testRowLevelPermission(self):
        """Tests for row(instance)-level permission-checking"""
        article = self.article
        book = self.book                
        user = self.user
        
        # No context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article)
        self.assertFalse(user.has_perm('VIEW', obj))
        # With context, model not subclassing  ``PermissionBase``
        obj = self._pack_context(article, website="FooSite")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(article, website="BarSite")
        self.assertTrue(user.has_perm('VIEW', obj))
        obj = self._pack_context(article, website="FooSite", edition="morning")
        self.assertTrue(user.has_perm('VIEW', obj))
        
        # No context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book)
        self.assertFalse(user.has_perm('VIEW', obj))
        # With context, model subclassing  ``PermissionBase``
        obj = self._pack_context(book, language="Italian")
        self.assertTrue(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="French")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="Dutch", cover="Paperback")
        self.assertTrue(user.has_perm('VIEW', obj)) 
        
    
    def testInheritedPermission(self):
        """A model subclassing ``PermissionBase`` should inherit all default permission-checking methods"""
        book = self.book                
        user = self.user
        
        # No context
        obj = self._pack_context(book)
        self.assertTrue(user.has_perm('DELETE', obj))
        # With context
        obj = self._pack_context(book, language="Italian")
        self.assertTrue(user.has_perm('DELETE', obj))
        obj = self._pack_context(book, language="Dutch", cover="Paperback")
        self.assertTrue(user.has_perm('DELETE', obj)) 
        
          
    def testOverridingPermission(self):
        """A model subclassing ``PermissionBase`` should be able to override any default permission-checking methods"""
        book = self.book                
        user = self.user
        
        # No context
        obj = self._pack_context(book)
        self.assertFalse(user.has_perm('VIEW', obj))
        # With context
        obj = self._pack_context(book, language="French")
        self.assertFalse(user.has_perm('VIEW', obj))
        obj = self._pack_context(book, language="English", cover="Paperback")
        self.assertFalse(user.has_perm('VIEW', obj)) 
        
    
class ObjectPermissionDecoratorTest(TestCase):
    """Tests for the ``object_permission_required()`` decorator"""
    
    def setUp(self):
        pass
        
    def testSuperUsersCanDoEverything(self):
        """Test that superusers always pass permission checks"""
        pass
    
    def testAnonymousUsersCanDoNothing(self):
        """Test that anonymous users always fail permission checks"""
        pass
    
    def testInactiveUsersCanDoNothing(self):
        """Test that inactive users always fail permission checks"""
        pass
    
    def testGlobalPermissionsDelegation(self):
        """If checking a non-object (global) permission, raise ``WrongPermissionCheck``"""
        pass
    
    def testWrongPermissionCheck(self):
        """If requesting a permission check not implemented by a model, raise ``WrongPermissionCheck`` """
        pass
    
    def testTableLevelPermission(self):
        """Tests for table(class)-level permission-checking"""
    
    def testRowLevelPermission(self):
        """Tests for row(instance)-level permission-checking"""
        pass
    
    def testInheritedPermission(self):
        """A model subclassing ``PermissionBase`` should inherit all default permission-checking methods"""
        pass
   
    def testOverridingPermission(self):
        """A model subclassing ``PermissionBase`` should be able to override any default permission-checking methods"""
        pass
    
    def testLoginURLNoRaise(self):
        """If the ``login_url`` parameter is set and ``raise_exception`` is ``False``, redirect to the login page if check fails"""
        pass 
    
    def testNoLoginURLNoRaise(self):
        """If the ``login_url`` parameter isn't set and ``raise_exception`` is ``False``, redirect to the default login page if check fails"""
        pass 
    
    def testLoginURLRaise(self):
        """If the ``login_url`` parameter is set but ``raise_exception`` is ``True``, raise ``PermissionDenied`` if check fails"""
        pass        
