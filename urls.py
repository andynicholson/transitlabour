from django.conf.urls.defaults import *

from transitlabourapp.views import page_view, blog_view, home_view, event_view, platform_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #admin
    (r'^admin/', include(admin.site.urls)),
    #static content, CSS, JS, images
    (r'^custom/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/andycat_/transitlabour.asia/transitlabour/templates/media'}),
    # the registration module
    (r'^accounts/', include('registration.backends.default.urls')),
    #profiles
    (r'^profiles/', include('profiles.urls')),

    #specific blog view
    (r'^blogs/(?P<slug_name>[-_\w]+)$', blog_view, {'author_name':None}),
    (r'^blogs/author/(?P<author_name>[-_\w]+)$', blog_view, {'slug_name':None}),

    #specific event view
    (r'^events/(?P<slug_name>[-_\w]+)$', event_view, {'author_name':None}),
 

    #home page
    (r'^$', home_view),
    (r'^home/$', home_view),

    #platforms
    (r'^sydney/$', platform_view,{'platform_name':'Sydney'}),
    (r'^kolkata/$', platform_view,{'platform_name':'Kolkata'}),
    (r'^shanghai/$', platform_view,{'platform_name':'Shanghai'}),

    #generic page views
    (r'^(?P<page_name>[a-z-]+)/$', page_view ),

    )
