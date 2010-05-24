from django.db import models
#from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.


class UserProfile(models.Model):
    # This is the only required field
    user = models.ForeignKey(User, unique=True)
    url=models.URLField(blank=True)

#
# News page
#
class Page(models.Model):
    parent=models.ForeignKey('self',blank=True,null=True)
    header=models.CharField(max_length=50)
    #page text attributes
    teaser_text=models.TextField()
    body=models.TextField(blank=True)
    background_image = models.ImageField(upload_to='bgimg/%Y/%m/%d', blank=True)
    published_date=models.DateTimeField(verbose_name='Date published', auto_now_add=True,blank=True,null=True)
    edited_date = models.DateTimeField(verbose_name='Date edited', auto_now=True,blank=True,null=True)
    slug = models.SlugField()
    menu_position = models.IntegerField(default=0)
    promoted = models.BooleanField()
    author = models.ForeignKey(User, related_name='userpages')

    def __unicode__(self):
        return u'%s' % (self.header)

    def get_absolute_url(self):
        return "/%s" % self.slug

    def is_editable_page(self):
	return True


#
# platform
#
class Platform(models.Model):
    name=models.CharField(max_length=50)

    def __unicode__(self):
    	return u'%s'%self.name


#
# Blog page
#
class Blog(models.Model):
    header=models.CharField(max_length=50)
    #page text attributes
    teaser_text=models.TextField()
    body=models.TextField(blank=True)
    background_image = models.ImageField(upload_to='bgimg/%Y/%m/%d', blank=True)
    published_date=models.DateTimeField(verbose_name='Date published', auto_now_add=True,blank=True,null=True)
    edited_date = models.DateTimeField(verbose_name='Date edited', auto_now=True,blank=True,null=True)
    slug = models.SlugField()
    promoted = models.BooleanField(verbose_name='Promoted to home page')
    author = models.ForeignKey(User, related_name='userblogs')
    sticky = models.BooleanField(verbose_name='Sticky on top of user blog')
    platform = models.ManyToManyField(Platform)
    promoted_platform = models.BooleanField(verbose_name='Promoted to platform home page')

    def __unicode__(self):
        return u'%s' % (self.header)

    def get_absolute_url(self):
        return "%s" % self.slug

    def is_editable_page(self):
	return True


#
# Event page
#
class Event(models.Model):
    header=models.CharField(max_length=50)
    #page text attributes
    teaser_text=models.TextField()
    body=models.TextField(blank=True)
    background_image = models.ImageField(upload_to='bgimg/%Y/%m/%d', blank=True)
    starting_date =models.DateTimeField(verbose_name='Starting time and date')
    ending_date = models.DateTimeField(verbose_name='Ending time and date')
    published_date=models.DateTimeField(verbose_name='Date published', auto_now_add=True,blank=True,null=True)
    edited_date = models.DateTimeField(verbose_name='Date edited', auto_now=True,blank=True,null=True)
    slug = models.SlugField()
    author = models.ForeignKey(User, related_name='userevents')

    def __unicode__(self):
        return u'%s' % (self.header)

    def get_absolute_url(self):
        return "%s" % self.slug

    def is_editable_page(self):
	return True


