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

from django.utils.translation import ugettext_lazy as _ 

import os
DIRNAME = os.path.dirname(__file__)

DEFAULT_CHARSET = 'utf-8'

test_engine = os.environ.get("FLEXI_AUTH_TEST_ENGINE", "django.db.backends.sqlite3")

DATABASES = {
    'default': {
        'ENGINE': test_engine,
        'NAME': os.environ.get("FLEXI_AUTH_DATABASE_NAME", "flexi_auth_test"),
        'USER': os.environ.get("FLEXI_AUTH_DATABASE_USER", ""),
        'PASSWORD': os.environ.get("FLEXI_AUTH_DATABASE_PASSWORD", ""),
        'HOST': os.environ.get("FLEXI_AUTH_DATABASE_HOST", "localhost"),
    }
}

if test_engine == "django.db.backends.sqlite3":
    DATABASES['default']['NAME'] = os.path.join(DIRNAME, 'flexi_auth_test.db')
    DATABASES['default']['HOST'] = ""
elif test_engine == "django.db.backends.mysql":
    DATABASES['default']['PORT'] = os.environ.get("FLEXI_AUTH_DATABASE_PORT", 3306)
elif test_engine == "django.db.backends.postgresql_psycopg2":
    DATABASES['default']['PORT'] = os.environ.get("FLEXI_AUTH_DATABASE_PORT", 5432)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions', 
    'django.contrib.sites',
    'django.contrib.flatpages',
    'permissions',
    'flexi_auth',
    'flexi_auth.tests',    
     # other dependencies go here 
)

MIDDLEWARE_CLASSES = (
     'django.middleware.common.CommonMiddleware',
     'django.contrib.sessions.middleware.SessionMiddleware',
     'django.contrib.auth.middleware.AuthenticationMiddleware',
     'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',                  
) 


ROOT_URLCONF = 'flexi_auth.tests.urls'
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
     'django.contrib.auth.backends.ModelBackend',
     'flexi_auth.backends.ParamRoleBackend',
)

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/accounts/profile/' 

# app-specific settings
ROLES_LIST = (
     ('EDITOR', _('Editor')),
     ('PUBLISHER', 'Publisher'),
     ('SPONSOR', 'Sponsor'),     
)

PARAM_CHOICES = (
     ('article', _('Article')),
     ('book', 'Book'),
     ('magazine', 'Magazine'),               
)

VALID_PARAMS_FOR_ROLES = {
     'EDITOR' : {'article': 'tests.Article'},
     'PUBLISHER' : {'book': 'tests.Book'},
     'SPONSOR' : {'article': 'tests.Article', 'magazine': 'tests.Magazine'}, 
}
