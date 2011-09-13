from django.test import TestCase
from django.contrib.auth.models import User, Group 

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
    """Test for the ``parametric_role_as_dict()`` helper function"""
    
    def setUp(self):
        pass
    
    def testConversionOK(self):
        """If a ``ParamRole`` instance is passed, return a dictionary representing it"""
        pass
    
    def testConversionFail(self):
        """If the argument isn't a ``ParamRole`` instance, raise a ``TypeError``"""
        pass
        
class ParamRoleAsDictValidationTest(TestCase):
    """Test for the ``_is_valid_parametric_role_dict_repr()`` helper function"""
    
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
    """Test for the ``_compare_parametric_roles()`` helper function"""
    
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
    """Test for the ``_validate_parametric_role`` function"""
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
    """Test for the ``register_parametric_role`` function"""
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
    
class RoleAutoSetupTest(TestCase):
    """Test automatic role-setup operations happening at instance-creation time"""

    def setUp(self):
        pass

class ParamRoleModelTest(TestCase):
    """Test basic behaviour of the ``ParamRole`` model"""

    def setUp(self):
        pass
    
    def testSingleParameterRetrieval(self):
        """Test ``ParamRole.param()`` method"""
        pass

class ParamRoleGetRoleTest(TestCase):
    """Test ``ParamRole.get_role()`` class method"""

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
    """Test ``ParamRole.add_principal()`` method"""

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
    """Test ``ParamRole.get_users()`` method"""
    
    def setUp(self):
        pass
    
    def testGetUsersOK(self):
        """Verify that all the users this parametric role was assigned to are returned"""
        pass
    
class ParamRoleGetGroupsTest(TestCase):
    """Test ``ParamRole.get_groups()`` method"""
    
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
    
    def testIsActiveOK(self):
        """Check that ``ParamRole.is_archived`` behaves as expected under normal conditions"""
        pass
    
    def testArchiveAPINotImplemented(self):
        """Check that ``ParamRole.is_(active|archived)`` behaves as expected if some parameter doesn't implement the 'archive API'"""
        pass

    
class PrincipalRoleRelationTest(TestCase):
    """Test for the ``PrincipalRoleRelation`` model methods"""
    
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
    """Test for the ``RoleManager`` custom manager class"""

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
    """Test for the ``ParamRoleBackend`` custom authorization backend"""

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
        """If checking a non-object (global) permission, return ``False``"""
        pass
    
    def testWrongUserArgument(self):
        """If ``user_obj`` is not an ``User`` instance, raise ``AttributeError`` """
        pass
    
    def testWrongPermissionCheck(self):
        """If requesting a permission check not implemented by a model, raise ``WrongPermissionCheck`` """
        pass
    
    def testTableLevelPermission(self):
        """Test for table(class)-level permission-checking"""
        pass
    
    def testTableLevelPermission(self):
        """Test for row(instance)-level permission-checking"""
        pass
    
    def testInheritedPermission(self):
        """A model subclassing ``PermissionBase`` should inherit all default permission-checking methods"""
        pass
          
    def testOverridingPermission(self):
        """A model subclassing ``PermissionBase`` should be able to override any default permission-checking methods"""
        pass
    

        

        









    



    
