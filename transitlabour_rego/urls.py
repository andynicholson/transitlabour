from django.conf.urls.defaults import *
from registration.views import register

from transitlabour_rego.forms import RecaptchaRegistrationForm

urlpatterns = patterns('',
    url(r'^register/$', register, {'backend':'registration.backends.default.DefaultBackend', 'form_class': RecaptchaRegistrationForm}, name='registration_register'),
    #(r'', include('registration.urls')),
     (r'', include('registration.backends.default.urls')),
)

