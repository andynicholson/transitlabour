from django.conf.urls.defaults import *

from transitlabourapp.views import page_view

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^transitlabour/', include('transitlabour.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^$', page_view, {'page_name':'home'}),
    (r'^(?P<page_name>[a-z-]+)/$', page_view ),

    (r'^custom/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/andycat_/transitlabour.asia/transitlabour/templates/media'}),

    (r'^accounts/', include('registration.backends.default.urls')),

)
