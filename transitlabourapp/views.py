
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404,HttpResponseNotFound
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.template import TemplateDoesNotExist
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.list_detail import object_list, object_detail
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth.models import User

from transitlabour.transitlabourapp.models import Page

def page_view(request, page_name):
	bloggers = User.objects.all()
	extra_context = {'bloggers':bloggers}
	if page_name == 'home':
		template_file_name=page_name
	else:
		template_file_name='about'
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )
