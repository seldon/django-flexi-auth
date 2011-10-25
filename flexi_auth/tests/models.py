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

from django.db import models

from flexi_auth.models import PermissionBase

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

class Magazine(models.Model):
    name = models.CharField(max_length=50)
    printing = models.IntegerField()

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(Author)
    published_to = models.ManyToManyField(Magazine)
    
    def __unicode__(self):
        return "An article with title '%s'" % self.title
    
    ##-------------- authorization API----------------##
    # table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
#        print "Now entering ``can_create`` method of model ``Article``..."
#        print "Executing check for permission 'CREATE' on model %(cls)s for user %(user)s wrt context %(ctx)s"\
#              % {'cls':cls, 'user':user, 'ctx':context}  
        if context:
            website = context.get('website', None)
            edition = context.get('edition', None)
            if (website=="BarSite" or (website=="FooSite" and edition=="morning")):
                return True                        
        return False 
    # row-level VIEW permission
    def can_view (self, user, context):
#        print "Now entering ``can_view`` method of model ``Article``..."
#        print "Executing check for permission 'VIEW' on instance %(self)s for user %(user)s wrt context %(ctx)s"\
#             % {'self':self, 'user':user, 'ctx':context}
        if context:
            website = context.get('website', None)
            edition = context.get('edition', None)
            if (website=="BarSite" or (website=="FooSite" and edition=="morning")):
                return True               
        return False 
    ##-------------------------------------------------##
    

class Book(models.Model, PermissionBase):
    title = models.CharField(max_length=50)
    content = models.TextField()
    authors = models.ManyToManyField(Author)
    
    def __unicode__(self):
        return "A book with title '%s'" % self.title
    
    
    ##-------------- authorization API----------------##
    # table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
#        print "Now entering ``can_create`` method of model ``Book``..."
#        print "Executing check for permission 'CREATE' on model %(cls)s for user %(user)s wrt context %(ctx)s"\
#              % {'cls':cls, 'user':user, 'ctx':context}  
        if context:
            language = context.get('language', None)
            cover = context.get('cover', None)
            if (language=="Italian" or (language=="Dutch" and cover=="Paperback")):
                return True         
        return False 
    # row-level VIEW permission
    def can_view (self, user, context):
#        print "Now entering ``can_view`` method of model ``Book``..."
#        print "Executing check for permission 'VIEW' on instance %(self)s for user %(user)s wrt context %(ctx)s"\
#             % {'self':self, 'user':user, 'ctx':context}
        if context:
            language = context.get('language', None)
            cover = context.get('cover', None)
            if (language=="Italian" or (language=="Dutch" and cover=="Paperback")):
                return True               
        return False 
    ##-------------------------------------------------##
        
