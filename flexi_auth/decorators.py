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

from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import user_passes_test

from flexi_auth.models import ObjectWithContext

def object_permission_required(perm, obj, login_url=None, raise_exception=False, **context):
    """
    Decorator for views that checks whether a user has been granted the permission ``perm``
    on the object ``obj`` with respect to the context ``context``.
    
    If the permission check fails, user will be redirected to the log-in page 
    (as specified by the ``login_url`` parameter) or, if the ``raise_exception`` parameter 
    is set to ``True``, the ``PermissionDenied`` exception will be raised instead.
    """
    # CREDITS: just adapting Django's built-in ``@permission_required()`` decorator
    def check_perms(user):
        # First check if the user has the permission (even anonymous users)
        contextual_obj = ObjectWithContext(obj, context)
        if user.has_perm(perm, contextual_obj):
            return True
        # In case the 403 handler should be called raise the exception
        if raise_exception:
            raise PermissionDenied
        # As the last resort, show the login form
        return False
    return user_passes_test(check_perms, login_url=login_url)
