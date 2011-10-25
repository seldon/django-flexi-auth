# Copyright (C) 2011 REES Marche <http://www.reesmarche.org>
#
# This file is part of ``django-flexi-auth``.

# ``django-flexi-auth`` is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# ``django-flexi-auth`` is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with ``django-flexi-auth``. If not, see <http://www.gnu.org/licenses/>.

from django.test import TestCase
from django.db import IntegrityError 
from django.contrib.auth.models import User, Group, AnonymousUser 
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import SESSION_KEY

from permissions.models import Role

from flexi_auth.utils import get_ctype_from_model_label, register_parametric_role, _parametric_role_as_dict,\
_is_valid_parametric_role_dict_repr, _compare_parametric_roles

from flexi_auth.exceptions import WrongPermissionCheck 
from flexi_auth.models import ObjectWithContext, Param, ParamRole
from flexi_auth.decorators import object_permission_required
from flexi_auth.exceptions import RoleParameterNotAllowed

from flexi_auth.tests import settings
from flexi_auth.tests.models import Article, Book, Author, Magazine
from flexi_auth.tests.views import CallableView, normal_view




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
        self.author1 = Author.objects.create(name="Bilbo", surname="Baggins")
        self.author2 = Author.objects.create(name="Luke", surname="Skywalker")
        
        self.magazine1 = Magazine.objects.create(name="Lorem Magazine", printing=1)
        self.magazine2 = Magazine.objects.create(name="Ipsum Magazine", printing=100)
        
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author1)
        self.article.published_to.add(self.magazine1, self.magazine2)
        self.article.save()
        
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        self.book.authors.add(self.author1, self.author2)
        self.book.save()
            
        self.pr1 = register_parametric_role('EDITOR', article=self.article)
        self.pr2 = register_parametric_role('PUBLISHER', book=self.book)
        self.pr3 = register_parametric_role('SPONSOR', article=self.article, magazine=self.magazine1)        
#    
    def testGetOK(self):
        """Verify that an existing parameter can be retrieved by its name"""
        self.assertEqual(self.pr1.article, self.article)
        self.assertEqual(self.pr2.book, self.book)
        self.assertEqual(self.pr3.article, self.article)
        self.assertEqual(self.pr3.magazine, self.magazine1)

    def testGetFailIfParameterNotSet(self):
        """When trying to retrieve an unset parameter, raise ``AttributeError``"""
        self.assertRaises(AttributeError, lambda x: self.pr1.book, 1)
        self.assertRaises(AttributeError, lambda x: self.pr2.article, 1)
        self.assertRaises(AttributeError, lambda x: self.pr3.book, 1)


class ParamModelTest(TestCase):
    """Test behaviour of the ``Param`` model"""

    def setUp(self):
        author = Author.objects.create(name="Bilbo", surname="Baggins")
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=author)
    
    def testParamUniqueness(self):
        """No duplicated ``Param``'s instances should exist in the DB"""
        Param.objects.create(name='article', value=self.article)
        self.assertRaises(IntegrityError, Param.objects.create, name='article', value=self.article)

class ParamRoleAsDictTest(TestCase):
    """Tests for the ``parametric_role_as_dict()`` helper function"""
    
    def setUp(self):
        self.author1 = Author.objects.create(name="Bilbo", surname="Baggins")
        self.author2 = Author.objects.create(name="Luke", surname="Skywalker")
        
        self.magazine1 = Magazine.objects.create(name="Lorem Magazine", printing=1)
        self.magazine2 = Magazine.objects.create(name="Ipsum Magazine", printing=100)
        
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author1)
        self.article.published_to.add(self.magazine1, self.magazine2)
        self.article.save()
        
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        self.book.authors.add(self.author1, self.author2)
        self.book.save()
    
        
        self.pr1 = register_parametric_role('EDITOR', article=self.article)
        self.pr2 = register_parametric_role('PUBLISHER', book=self.book)
        self.pr3 = register_parametric_role('SPONSOR', article=self.article, magazine=self.magazine1)     
    
    def testConversionOK(self):
        """If a ``ParamRole`` instance is passed, return a dictionary representing it"""
        role = Role.objects.get(name='EDITOR')
        expected_dict = {'role':role, 'params':{'article': self.article}}
        self.assertEqual(_parametric_role_as_dict(self.pr1), expected_dict)
        
        role = Role.objects.get(name='PUBLISHER')
        expected_dict = {'role':role, 'params':{'book': self.book}}
        self.assertEqual(_parametric_role_as_dict(self.pr2), expected_dict)
        
        role = Role.objects.get(name='SPONSOR')
        expected_dict = {'role':role, 'params':{'article': self.article, 'magazine': self.magazine1}}
        self.assertEqual(_parametric_role_as_dict(self.pr3), expected_dict)   
    
    
    def testConversionFail(self):
        """If the argument isn't a ``ParamRole`` instance, raise a ``TypeError``"""
        role = Role.objects.get(name='EDITOR')
        self.assertRaises(TypeError, _parametric_role_as_dict, None)
        self.assertRaises(TypeError, _parametric_role_as_dict, 1)
        self.assertRaises(TypeError, _parametric_role_as_dict, role)

        
class ParamRoleAsDictValidationTest(TestCase):
    """Tests for the ``_is_valid_parametric_role_dict_repr()`` helper function"""
    
    def setUp(self):
        self.role = Role.objects.create(name='SPONSOR')
        self.author = Author.objects.create(name="Bilbo", surname="Baggins")
        self.magazine = Magazine.objects.create(name="Lorem Magazine", printing=1)
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author)
        
    
    def testValidationOK(self):
        """If a dictionary has the right structure to represent a parametric role, return ``True``"""
        p_role_dict = {'role':self.role, 'params':{'article': self.article, 'magazine': self.magazine}}
        self.assertTrue(_is_valid_parametric_role_dict_repr(p_role_dict))
    
    def testValidationFailIfNotDict(self): 
        """If passed dictionary hasn't expected keys, return ``False``  """
        p_role_dict = {'foo':self.role, 'params':{'article': self.article, 'magazine': self.magazine}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
        
        p_role_dict = {'role':self.role, 'foo':{'article': self.article, 'magazine': self.magazine}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
        
        p_role_dict = {'role':self.role, 'params':{'article': self.article, 'magazine': self.magazine}, 'foo':None}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))
    
    def testValidationFailIfNotRole(self): 
        """If ``role`` key is not a ``Role`` model instance, return ``False``"""
        p_role_dict = {'role':1, 'params':{'article': self.article, 'magazine': self.magazine}}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict))        

    def testValidationFailIfNotParams(self): 
        """If ``params`` key is not a dictionary, return ``False``"""
        p_role_dict = {'role':self.role, 'params':1}
        self.assertFalse(_is_valid_parametric_role_dict_repr(p_role_dict)) 

        
class ParamRoleComparisonTest(TestCase):
    """Tests for the ``_compare_parametric_roles()`` helper function"""
    
    def setUp(self):
        self.author = Author.objects.create(name="Bilbo", surname="Baggins")
        self.magazine = Magazine.objects.create(name="Lorem Magazine", printing=1)
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author)
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        
        self.role1 = Role.objects.create(name='FOO')
        self.role2 = Role.objects.create(name='BAR')
              
        self.p1 = Param.objects.create(name='magazine', value=self.magazine)
        self.p2 = Param.objects.create(name='article', value=self.article)
        self.p3 = Param.objects.create(name='book', value=self.book)
        
        pr1 = ParamRole.objects.create(role=self.role1)
        pr1.param_set.add(self.p1)
        pr1.param_set.add(self.p2)
        pr1.save()
        self.pr1 = pr1
        
        pr2 = ParamRole.objects.create(role=self.role1)
        pr2.param_set.add(self.p1)
        pr2.param_set.add(self.p2)
        pr2.save()
        self.pr2 = pr2
        
        pr3 = ParamRole.objects.create(role=self.role2)
        pr3.param_set.add(self.p1)
        pr3.param_set.add(self.p2)
        pr3.save()
        self.pr3 = pr3
        
        pr4 = ParamRole.objects.create(role=self.role1)
        pr4.param_set.add(self.p3)
        pr4.param_set.add(self.p2)
        pr4.save()
        self.pr4 = pr4 
    
    def testComparisonOK(self):
        """If arguments describe the same parametric role, return ``True``"""
        # compare two ParamRole instances
        self.assertTrue(_compare_parametric_roles(self.pr1, self.pr2))
                
        # compare two dictionary representations
        p_role_dict_1 = {'role':self.role1, 'params':{'article': self.article, 'magazine': self.magazine}}
        p_role_dict_2 = {'role':self.role1, 'params':{'magazine': self.magazine, 'article': self.article}}
        self.assertTrue(_compare_parametric_roles(p_role_dict_1, p_role_dict_2))
        
        # compare one ParamRole instance and one dictionary representation
        self.assertTrue(_compare_parametric_roles(p_role_dict_1, self.pr2))
        self.assertTrue(_compare_parametric_roles(p_role_dict_2, self.pr1))
    
    def testFailIfNotSameKind(self):
        """If arguments describe parametric roles of different kind, return ``False``"""
        self.assertFalse(_compare_parametric_roles(self.pr1, self.pr3))
    
    def testFailIfNotSameParameters(self):
        """If arguments describe parametric roles with different parameters, return ``False``"""
        self.assertFalse(_compare_parametric_roles(self.pr1, self.pr4))
    
    def testErrorIfTooManyArguments(self): 
        """If more than two arguments are given, raise ``TypeError``"""
        self.assertRaises(TypeError, _compare_parametric_roles, self.pr1, self.pr2, self.pr2)
        self.assertRaises(TypeError, _compare_parametric_roles, self.pr1, self.pr2, None)
    
    def testErrorIfNotEnoughArguments(self):
        """If less than two arguments are given, raise ``TypeError``"""
        self.assertRaises(TypeError, _compare_parametric_roles, self.pr1)
        self.assertRaises(TypeError, _compare_parametric_roles)
    
    def testErrorIfInvalidArguments(self):
        """If an argument is neither a ParamRole instance nor a valid dictionary representation for it, raise ``TypeError``"""
        self.assertRaises(TypeError, _compare_parametric_roles, self.pr1, None)
        self.assertRaises(TypeError, _compare_parametric_roles, None, self.pr1)
        self.assertRaises(TypeError, _compare_parametric_roles, self.pr1, {})
        self.assertRaises(TypeError, _compare_parametric_roles, {}, self.pr1)
        
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
        """If the name of parameter is invalid ``.is_(active|archived)`` should raise RoleParameterNotAllowed"""
        pass
    
    def testArchiveAPIFailIfInvalidParamType(self):
        """If the value of a parameter is of the wrong type, ``.is_(active|archived)`` should raise RoleParameterWrongSpecsProvided"""
        pass 
       

class ParamRoleBackendTest(TestCase):
    """Tests for the ``ParamRoleBackend`` custom authorization backend"""

    def setUp(self):
        self.user = User.objects.create_user(username="Ian Solo", email="ian@rebels.org", password="secret")
        
        harry = User.objects.create_user(username="Harry Potter", email="harry@hogwarts.uk", password="secret")
        harry.is_superuser=True
        harry.save()
        self.super_user = harry
               
        self.anon_user = AnonymousUser()
        
        albus = User.objects.create_user(username="Albus Silente", email="albus@hogwarts.uk", password="secret")
        albus.is_active=False
        albus.save()
        self.inactive_user = albus        
        
        self.author1 = Author.objects.create(name="Bilbo", surname="Baggins")
        self.author2 = Author.objects.create(name="Luke", surname="Skywalker")
        
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author1)
        
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        self.book.authors.add(self.author1, self.author2)
        self.book.save()
        
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
        
        ## Superusers by-pass all access-control checks, so there is no simple way
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
    
    # some test URLs
    base_test_urls = (
           '/no-inheritance/table/no-context/',    
           '/no-inheritance/table/with-context/1/',
           '/no-inheritance/table/with-context/2/',
           '/no-inheritance/table/with-context/3/',
           '/inheritance/table/no-context/',    
           '/inheritance/table/with-context/1/',
           '/inheritance/table/with-context/2/',
           '/inheritance/table/with-context/3/',
           '/no-inheritance/row/no-context/',    
           '/no-inheritance/row/with-context/1/',
           '/no-inheritance/row/with-context/2/',
           '/no-inheritance/row/with-context/3/',
           '/inheritance/row/no-context/',    
           '/inheritance/row/with-context/1/',
           '/inheritance/row/with-context/2/',
           '/inheritance/row/with-context/3/',
            )
    
    # which subset of the test URLs a 'regular' user is granted access to
    base_allowed_urls = (
               )
    # which subset of the test URLs a 'regular' user is denied access to          
    base_denied_urls = (              
              )
    ##------------------------------- Helper methods --------------------------------##    
    def get_test_urls(self, prefix, kind='ALL'):

        if kind == 'ALL':            
            urls = [prefix + url for url in self.base_test_urls]            
        elif kind == 'ALLOWED':
            urls = [prefix + url for url in self.base_allowed_urls]
        elif kind == 'DENIED':
            urls = [prefix + url for url in self.base_denied_urls]
        else: 
            raise TypeError("%s is not a valid value for the `kind` argument; allowed values are 'ALL', 'ALLOWED', 'DENIED' ." % kind)
        
        return urls
    
    def get_url_prefix_from_decorator_args(self, login_url, raise_exception):
        if raise_exception:
            url_prefix = '/restricted_raise'
        elif login_url:
            url_prefix = '/restricted_login'
        else:
            url_prefix = '/restricted'  
         
        return url_prefix    
    
    def check_url_access(self, user, allowed_urls, forbidden_urls, login_url=None, raise_exception=False):
        
        if not user.is_anonymous():
            self.login(user)
        
        for url in allowed_urls:
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200, msg="Failed permission check for URL %s" % url)
        
        for url in forbidden_urls:
            if raise_exception:
                self.assertRaises(WrongPermissionCheck, self.client.get, url)
            elif not login_url:
                login_url = settings.LOGIN_URL
            else:            
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(login_url in response['Location'])             
        self.client.logout()    
    
    def login(self, user_obj, password='secret'):
        response = self.client.post('/login/', {
            'username': user_obj.username,
            'password': password
                }
            )
    
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].endswith(settings.LOGIN_REDIRECT_URL))
        self.assertTrue(SESSION_KEY in self.client.session)
    ##-------------------------------------------------------------------------------##
    
    
    def setUp(self):
        self.user = User.objects.create_user(username="Ian Solo", email="ian@rebels.org", password="secret")
        
        harry = User.objects.create_user(username="Harry Potter", email="harry@hogwarts.uk", password="secret")
        harry.is_superuser=True
        harry.save()
        self.super_user = harry
               
        self.anon_user = AnonymousUser()
        
        albus = User.objects.create_user(username="Albus Silente", email="albus@hogwarts.uk", password="secret")
        albus.is_active=False
        albus.save()
        self.inactive_user = albus        
        
        self.author1 = Author.objects.create(name="Bilbo", surname="Baggins")
        self.author2 = Author.objects.create(name="Luke", surname="Skywalker")
        
        self.article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=self.author1)
        
        self.book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
        self.book.authors.add(self.author1, self.author2)
        self.book.save()
    
    def tearDown(self):
        pass    
           
    def testCallable(self):
        """
        Check that ``object_permission_required()`` is assignable to callable objects.
        """
        article = self.article
        
        object_permission_required("FOO", article)(CallableView)
        object_permission_required("FOO", article, website='www.example.com')(CallableView)        
        object_permission_required("FOO", article, website='www.example.com', edition='morning')(CallableView)
    
    def testView(self):
        """
        Check that ``object_permission_required()`` is assignable to 'regular' views.
        """
        article = self.article
    
        object_permission_required("FOO", article)(normal_view)
        object_permission_required("FOO", article, website='www.example.com')(normal_view)        
        object_permission_required("FOO", article, website='www.example.com', edition='morning')(normal_view)    
    
        
    def testSuperUsersCanDoEverything(self, login_url=None, raise_exception=False):
        """Test that superusers always pass permission checks"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)                        
        user = self.super_user
        allowed_urls = self.get_test_urls(prefix=url_prefix)
        forbidden_urls = ()
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)
           
        
    def testAnonymousUsersCanDoNothing(self, login_url=None, raise_exception=False):
        """Test that anonymous users always fail permission checks"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)
        user = self.anon_user
        allowed_urls = ()
        forbidden_urls = self.get_test_urls(prefix=url_prefix)
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)
              
        
    def testInactiveUsersCanDoNothing(self, login_url=None, raise_exception=False):
        """Test that inactive users always fail permission checks"""
        
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)           
        user = self.inactive_user
        allowed_urls = ()
        forbidden_urls = self.get_test_urls(prefix=url_prefix)
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)
        
        
    def testGlobalPermissionsDelegation(self, login_url=None, raise_exception=False):
        """If checking a non-object (global) permission, raise ``WrongPermissionCheck``"""
        pass
    
    def testWrongPermissionCheck(self, login_url=None, raise_exception=False):
        """If requesting a permission check not implemented by a model, raise ``WrongPermissionCheck`` """
        pass
    
    def testTableLevelPermission(self, login_url=None, raise_exception=False):
        """Tests for table(class)-level permission-checking"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)                 
        user = self.user
        allowed_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='ALLOWED') if ('/table/' in url)]
        forbidden_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='DENIED') if ('/table/' in url)]
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)
        
    def testRowLevelPermission(self, login_url=None, raise_exception=False):
        """Tests for row(instance)-level permission-checking"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)                 
        user = self.user
        allowed_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='ALLOWED') if ('/row/' in url)]
        forbidden_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='DENIED') if ('/row/' in url)]
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)        
    
    def testInheritedPermission(self, login_url=None, raise_exception=False):
        """A model subclassing ``PermissionBase`` should inherit all default permission-checking methods"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)                 
        user = self.user
        # FIXME: check if test is representative !
        allowed_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='ALLOWED') if ('/inheritance/' in url)]
        forbidden_urls = [url for url in self.get_test_urls(prefix=url_prefix, kind='DENIED') if ('/inheritance/' in url)]
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)        
    
   
    def testOverridingPermission(self, login_url=None, raise_exception=False):
        """A model subclassing ``PermissionBase`` should be able to override any default permission-checking methods"""
        url_prefix = self.get_url_prefix_from_decorator_args(login_url, raise_exception)                 
        user = self.user
        allowed_urls = () # FIXME
        forbidden_urls = () # FIXME
        self.check_url_access(user, allowed_urls, forbidden_urls, login_url, raise_exception)        
    
