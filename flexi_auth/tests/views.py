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

from django.http import HttpResponse

def normal_view(request):
    """
    A dummy 'regular' view
    """
    pass

class CallableView(object):
    """
    A dummy callable object to be used as a view
    """
    def __call__(self, *args, **kwargs):
        pass

def restricted_view(request):
    """
    Just a dummy view to test ``@object_permission_required`` decorator
    """
    return HttpResponse()
    
