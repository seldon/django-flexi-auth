from django.db import models

from flexi_auth.models import PermissionBase

class Author(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)

class Article(models.Model):
    title = models.CharField(max_length=50)
    body = models.TextField()
    author = models.ForeignKey(Author)
    
    ##-------------- authorization API----------------##
    # table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        if context:
            try:
                website = context['website']
                edition = context['edition']
                if (website=="BarSite" or (website=="FooSite" and edition=="morning")):
                    return True               
            except KeyError:
                pass         
        return False 
    # row-level VIEW permission
    def can_view (self, user, context):
        if context:
            try:
                website = context['website']
                edition = context['edition']
                if (website=="BarSite" or (website=="FooSite" and edition=="morning")):
                    return True               
            except KeyError:
                pass         
        return False 
    ##-------------------------------------------------##
    

class Book(models.Model, PermissionBase):
    title = models.CharField(max_length=50)
    content = models.TextField()
    authors = models.ManyToManyField(Author)
    
    ##-------------- authorization API----------------##
    # table-level CREATE permission
    @classmethod
    def can_create(cls, user, context):
        if context:
            try:
                website = context['website']
                edition = context['edition']
                if (website=="BarSite" or (website=="FooSite" and edition=="morning")):
                    return True               
            except KeyError:
                pass         
        return False 
    # row-level VIEW permission
    def can_view (self, user, context):
        if context:
            try:
                language = context['language']
                cover = context['cover']
                if (language=="Italian" or (language=="Dutch" and cover=="Paperback")):
                    return True               
            except KeyError:
                pass         
        return False 
    ##-------------------------------------------------##
        