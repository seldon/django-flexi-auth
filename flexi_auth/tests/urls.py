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

from django.conf.urls.defaults import patterns
from django.contrib.auth.urls import urlpatterns

from flexi_auth.decorators import object_permission_required

from flexi_auth.tests.views import restricted_view
from flexi_auth.tests.models import Article, Author, Book

# Just a bit of environment for tests 
author1 = Author.objects.create(name="Bilbo", surname="Baggins")
author2 = Author.objects.create(name="Luke", surname="Skywalker")
article = Article.objects.create(title="Lorem Ipsum", body="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...", author=author1)
book = Book.objects.create(title="Lorem Ipsum - The book", content="Neque porro quisquam est qui dolorem ipsum quia dolor sit amet...")
book.authors.add(author1, author2)
book.save()
    
# in case the  permission check fails, redirect to ``settings.LOGIN_REDIRECT_URL``
urlpatterns = urlpatterns + patterns('',
     (r'^restricted/no-inheritance/table/no-context/$', object_permission_required('CREATE', Article)(restricted_view)),
     (r'^restricted/no-inheritance/table/with-context/1/$', object_permission_required('CREATE', Article, website="FooSite")(restricted_view)),
     (r'^restricted/no-inheritance/table/with-context/2/$', object_permission_required('CREATE', Article, website="BarSite")(restricted_view)),
     (r'^restricted/no-inheritance/table/with-context/3/$', object_permission_required('CREATE', Article, website="FooSite", edition="morning")(restricted_view)),
     (r'^restricted/inheritance/table/no-context/$', object_permission_required('CREATE', Book)(restricted_view)),
     (r'^restricted/inheritance/table/with-context/1/$', object_permission_required('CREATE', Book, language="Italian")(restricted_view)),
     (r'^restricted/inheritance/table/with-context/2/$', object_permission_required('CREATE', Book, language="French")(restricted_view)),
     (r'^restricted/inheritance/table/with-context/3/$', object_permission_required('CREATE', Book, language="Dutch", cover="Paperback")(restricted_view)),
     (r'^restricted/no-inheritance/row/no-context/$', object_permission_required('VIEW', article)(restricted_view)),
     (r'^restricted/no-inheritance/row/with-context/1/$', object_permission_required('VIEW', article, website="FooSite")(restricted_view)),
     (r'^restricted/no-inheritance/row/with-context/2/$', object_permission_required('VIEW', article, website="BarSite")(restricted_view)),
     (r'^restricted/no-inheritance/row/with-context/3/$', object_permission_required('VIEW', article, website="FooSite", edition="morning")(restricted_view)),
     (r'^restricted/inheritance/row/no-context/$', object_permission_required('VIEW', book)(restricted_view)),
     (r'^restricted/inheritance/row/with-context/1/$', object_permission_required('VIEW', book, language="Italian")(restricted_view)),
     (r'^restricted/inheritance/row/with-context/2/$', object_permission_required('VIEW', book, language="French")(restricted_view)),
     (r'^restricted/inheritance/row/with-context/3/$', object_permission_required('VIEW', book, language="Dutch", cover="Paperback")(restricted_view)),
     
) 

# in case the permission check fails, redirect to a user-defined ``login_url``

urlpatterns = urlpatterns + patterns('',
     (r'^restricted_login/no-inheritance/table/no-context/$', object_permission_required('CREATE', Article, login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/table/with-context/1/$', object_permission_required('CREATE', Article, website="FooSite", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/table/with-context/2/$', object_permission_required('CREATE', Article, website="BarSite", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/table/with-context/3/$', object_permission_required('CREATE', Article, website="FooSite", edition="morning", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/table/no-context/$', object_permission_required('CREATE', Book, login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/table/with-context/1/$', object_permission_required('CREATE', Book, language="Italian", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/table/with-context/2/$', object_permission_required('CREATE', Book, language="French", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/table/with-context/3/$', object_permission_required('CREATE', Book, language="Dutch", cover="Paperback", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/row/no-context/$', object_permission_required('VIEW', article, login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/row/with-context/1/$', object_permission_required('VIEW', article, website="FooSite", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/row/with-context/2/$', object_permission_required('VIEW', article, website="BarSite", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/no-inheritance/row/with-context/3/$', object_permission_required('VIEW', article, website="FooSite", edition="morning", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/row/no-context/$', object_permission_required('VIEW', book,  login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/row/with-context/1/$', object_permission_required('VIEW', book, language="Italian", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/row/with-context/2/$', object_permission_required('VIEW', book, language="French", login_url='/somewhere/')(restricted_view)),
     (r'^restricted_login/inheritance/row/with-context/3/$', object_permission_required('VIEW', book, language="Dutch", cover="Paperback", login_url='/somewhere/')(restricted_view)),
)

# in case the  permission check fails, raise a ``Permission Denied`` exception
urlpatterns = urlpatterns + patterns('',
     (r'^restricted_raise/no-inheritance/table/no-context/$', object_permission_required('CREATE', Article)(restricted_view)),
     (r'^restricted_raise/no-inheritance/table/with-context/1/$', object_permission_required('CREATE', Article, website="FooSite", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/table/with-context/2/$', object_permission_required('CREATE', Article, website="BarSite", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/table/with-context/3/$', object_permission_required('CREATE', Article, website="FooSite", edition="morning", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/table/no-context/$', object_permission_required('CREATE', Book, raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/table/with-context/1/$', object_permission_required('CREATE', Book, language="Italian", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/table/with-context/2/$', object_permission_required('CREATE', Book, language="French", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/table/with-context/3/$', object_permission_required('CREATE', Book, language="Dutch", cover="Paperback", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/row/no-context/$', object_permission_required('VIEW', article, raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/row/with-context/1/$', object_permission_required('VIEW', article, website="FooSite", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/row/with-context/2/$', object_permission_required('VIEW', article, website="BarSite", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/no-inheritance/row/with-context/3/$', object_permission_required('VIEW', article, website="FooSite", edition="morning", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/row/no-context/$', object_permission_required('VIEW', book, raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/row/with-context/1/$', object_permission_required('VIEW', book, language="Italian", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/row/with-context/2/$', object_permission_required('VIEW', book, language="French", raise_exception=True)(restricted_view)),
     (r'^restricted_raise/inheritance/row/with-context/3/$', object_permission_required('VIEW', book, language="Dutch", cover="Paperback", raise_exception=True)(restricted_view)),
)
