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

from django.utils.translation import ugettext as _

class RoleNotAllowed(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return _(u"Role %s is not allowed in current application domain") % self.value

class RoleParameterNotAllowed(Exception):

    def __init__(self, role_name, allowed_params, wrong_param):
        self.role_name = role_name
        self.allowed_params = allowed_params
        self.wrong_param = wrong_param

    def __str__(self):
        return _(u"Wrong param '%(wp)s' provided for role %(r)s. Only %(pl)s are relatable to this role") % \
                  { 'wp' : self.wrong_param, 'r' : self.role_name, 'pl' : ", ".join(self.allowed_params) }


class RoleParameterWrongSpecsProvided(Exception):
    def __init__(self, role_name, param_specs):

        self.role_name = role_name
        self.param_specs = param_specs

    def __str__(self):
        return _(u"Wrong specs %(s)s for role %(r)s") % \
                    { 's' : self.param_specs, 'r' : self.role_name }

class WrongPermissionCheck(Exception):
    def __init__(self, perm, obj, context):
        self.perm = perm
        self.obj = obj
        self.context = context

    def __str__(self):
        return _(u"Can't check permission %(perm)s on object %(obj)s with respect to context %(ctx)s") % \
                    { 'perm' : self.perm, 'obj' : self.obj, 'ctx' : self.context }
    
    
    
