from django.db import models
#from django_extensions.db.fields import AutoSlugField
from django.contrib.auth.models import User

# Create your models here.
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
    author = models.ForeignKey(User, related_name='pages')

    def __unicode__(self):
        return u'%s' % (self.header)

    def get_absolute_url(self):
        return "/%s" % self.slug

    def is_editable_page(self):
	return True



