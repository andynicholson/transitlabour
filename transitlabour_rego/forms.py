from django import forms
from transitlabourapp import fields as transitlabour_fields
from registration.forms import RegistrationForm

class RecaptchaRegistrationForm(RegistrationForm):
    recaptcha = transitlabour_fields.ReCaptchaField()

