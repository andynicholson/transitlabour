from django.conf.urls.defaults import *

from transitlabourapp.views import page_view, blog_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #admin
    (r'^admin/', include(admin.site.urls)),
    #generic page views
    (r'^$', page_view, {'page_name':'home'}),
    (r'^(?P<page_name>[a-z-]+)/$', page_view ),
    #specific blog view
    (r'^blogs/(?P<slug_name>[-_\w]+)$', blog_view, {'author_name':None}),
    (r'^blogs/author/(?P<author_name>[-_\w]+)$', blog_view, {'slug_name':None}),

    #static content, CSS, JS, images
    (r'^custom/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/andycat_/transitlabour.asia/transitlabour/templates/media'}),
    # the registration module
    (r'^accounts/', include('registration.backends.default.urls')),

)
