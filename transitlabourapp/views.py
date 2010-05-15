
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

from transitlabour.transitlabourapp.models import Page, Blog

def blog_view(request, slug_name, author_name):
	bloggers = User.objects.all()
	#find the required blog via its slug 'slug_name'

	if not slug_name is None:
		blogs = Blog.objects.all().order_by('published_date').filter(slug=slug_name)
		author_view = False
		blog_view = True
		bauthor = None
	else:
		bauthor = User.objects.all().filter(username=author_name)[0]
		blogs = Blog.objects.all().order_by('published_date').filter(author=bauthor)
		author_view = True
		blog_view = False

	extra_context = {'bloggers':bloggers, 'blogs':blogs, 'blog_view':blog_view, 'author_view':author_view, 'bauthor':bauthor}

	template_file_name='blogs'
	page_name='blogs'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def page_view(request, page_name):
	bloggers = User.objects.all()
	blogs = Blog.objects.all().order_by('published_date')
	extra_context = {'bloggers':bloggers, 'blogs':blogs}

	#decide which template file to use based on page name
	if page_name == 'home' or page_name=='blogs':
		template_file_name=page_name
	else:
		#generic template to use for all other pages
		template_file_name='about'
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )
