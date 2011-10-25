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

For running tests, issue the command:

{{{

django-admin.py test --settings=flexi_auth.tests.settings tests

}}}

To get more details from the test runner, add the ``-v 2`` flag:

{{{

django-admin.py test --settings=flexi_auth.tests.settings tests -v 2

}}}


Be sure that the ``flexi_auth`` package is on your Python import search path !


