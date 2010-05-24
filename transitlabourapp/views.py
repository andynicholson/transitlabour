
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

from transitlabour.transitlabourapp.models import Page, Blog, Event, Platform
import datetime

def platform_view(request, platform_name):
	bloggers = User.objects.all()
	#find the required blog via its slug 'slug_name'
	platform = Platform.objects.all().filter(name=platform_name)

	blogs = Blog.objects.all().filter(promoted_platform=True, platform=platform).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted_platform=False, platform=platform).order_by('-published_date')[:4]
	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('-starting_date')[:5]

	extra_context = {'bloggers':bloggers, 'pblogs':blogs, 'lblogs':lblogs, 'events':events }

	template_file_name='home'
	page_name='home'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def home_view(request):
	bloggers = User.objects.all()
	#find the required blog via its slug 'slug_name'

	blogs = Blog.objects.all().filter(promoted=True).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted=False).order_by('-published_date')[:4]
	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('-starting_date')[:5]

	extra_context = {'bloggers':bloggers, 'pblogs':blogs, 'lblogs':lblogs, 'events':events }

	template_file_name='home'
	page_name='home'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def blog_view(request, slug_name, author_name):
	bloggers = User.objects.all()
	#find the required blog via its slug 'slug_name'

	if not slug_name is None:
		blogs = Blog.objects.all().filter(slug=slug_name).order_by('-published_date')
		author_view = False
		blog_view = True
		bauthor = None
		sticky_blogs = None
	else:
		bauthor = User.objects.all().filter(username=author_name)[0]
		blogs = Blog.objects.all().filter(author=bauthor, sticky=False).order_by('-published_date')
		sticky_blogs = Blog.objects.all().filter(author=bauthor, sticky=True).order_by('-published_date')
		author_view = True
		blog_view = False

	extra_context = {'bloggers':bloggers, 'blogs':blogs, 'blog_view':blog_view, 'author_view':author_view, 'bauthor':bauthor, 'sticky_blogs':sticky_blogs}

	template_file_name='blogs'
	page_name='blogs'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def event_view(request, slug_name, author_name):
	bloggers = User.objects.all()
	#find the required blog via its slug 'slug_name'

	if not slug_name is None:
		events = Event.objects.all().filter(slug=slug_name).order_by('-starting_date')
		author_view = False
		event_view = True
		bauthor = None
	else:
		bauthor = User.objects.all().filter(username=author_name)[0]
		events = Event.objects.all().filter(author=bauthor).order_by('-starting_date')
		author_view = True
		event_view = False

	extra_context = {'bloggers':bloggers, 'events':events, 'event_view':event_view, 'author_view':author_view, 'bauthor':bauthor}

	template_file_name='events'
	page_name='events'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def page_view(request, page_name):
	bloggers = User.objects.all()
	blogs = Blog.objects.all().order_by('-published_date')
	events = Event.objects.all().order_by('-starting_date')
	extra_context = {'bloggers':bloggers, 'blogs':blogs, 'events':events}

	#decide which template file to use based on page name
	if page_name == 'home' or page_name=='blogs' or page_name=='events':
		template_file_name=page_name
	else:
		#generic template to use for all other pages
		template_file_name='about'
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

