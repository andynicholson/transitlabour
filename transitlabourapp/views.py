
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

OBJECTS_PER_PAGE = 4

def paginate(request,list,pagename='page'):
	paginator = Paginator(list, OBJECTS_PER_PAGE) # Show 2 events per page
        # Make sure page request is an int. If not, deliver first page.
        try:
                page = int(request.GET.get(pagename, '1'))
        except ValueError:
                page = 1

        # If page request (9999) is out of range, deliver last page of results.
        try:
                result_paginator = paginator.page(page)
        except (EmptyPage, InvalidPage):
                result_paginator = paginator.page(paginator.num_pages)
	return result_paginator


def platform_view(request, platform_name):
	#find the required blog via its slug 'slug_name'
	platform = Platform.objects.all().filter(name=platform_name)

	blogs = Blog.objects.all().filter(promoted_platform=True, platform=platform).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted_platform=False, platform=platform).order_by('-published_date')

	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('-starting_date')[:5]

	bloggers = latest_bloggers(lblogs)

   	#paginate results
        blog_paginator = paginate(request,lblogs)

	extra_context = {'bloggers':bloggers, 'pblogs':blogs, 'lblogs':blog_paginator, 'events':events , 'platformpage':True}

	template_file_name='home'
	page_name=platform_name
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def home_view(request):
	#find the required blog via its slug 'slug_name'

	blogs = Blog.objects.all().filter(promoted=True).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted=False).order_by('-published_date')
	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('-starting_date')[:5]

	bloggers = latest_bloggers(blogs)

	#paginate results
	blog_paginator = paginate(request,lblogs)

	extra_context = {'bloggers':bloggers, 'pblogs':blogs, 'lblogs':blog_paginator, 'events':events , 'homepage':True}

	template_file_name='home'
	page_name='home'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def blog_view(request, slug_name, author_name):
	# note - this is currently only used for a specfic blog view and author view - not the front page of the "blogs" section of the site
	# check urls.py carefully

	#find the required blog via its slug 'slug_name'
	if not slug_name is None:
		blogs = Blog.objects.all().filter(slug=slug_name).order_by('-published_date')
		author_view = False
		blog_view = True
		bauthor = None
		sticky_blogs = None
	else:
		#no slugname - author view
		bauthor = User.objects.all().filter(username=author_name)[0]
		blogs = Blog.objects.all().filter(author=bauthor, sticky=False).order_by('-published_date')
		sticky_blogs = Blog.objects.all().filter(author=bauthor, sticky=True).order_by('-published_date')
		author_view = True
		blog_view = False

	bloggers = latest_bloggers(blogs)

	#paginate results
	blog_paginator = paginate(request,blogs)

	extra_context = {'bloggers':bloggers, 'blogs':blog_paginator, 'blog_view':blog_view, 'author_view':author_view, 'bauthor':bauthor, 'sticky_blogs':sticky_blogs}

	template_file_name='blogs'
	page_name='blogs'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def event_view(request, slug_name, author_name):
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

	bloggers=[]
	extra_context = {'bloggers':bloggers, 'events':events, 'event_view':event_view, 'author_view':author_view, 'bauthor':bauthor}

	template_file_name='events'
	page_name='events'
	# find the Page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def page_view(request, page_name):
	blogs = Blog.objects.all().order_by('-published_date')
	events = Event.objects.all().order_by('-starting_date')
	bloggers = latest_bloggers(blogs)

	#paginate the blogs homepage
	blogs_paginator = paginate(request,blogs)

	extra_context = {'bloggers':bloggers, 'blogs':blogs_paginator, 'events':events}

	#decide which template file to use based on page name
	# ie - this view currently handles - home , blogs, and events top level pages
	if page_name == 'home' or page_name=='blogs' or page_name=='events':
		template_file_name=page_name
	else:
		#generic template to use for all other pages
		template_file_name='about'
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def latest_bloggers(blogs):
        bloggers = []
        for lblog in blogs:
                skip = False
                for b in bloggers:
                        if b == lblog.author:
                                skip = True
                                break
                if not skip:
                        bloggers.append(lblog.author)
	return bloggers
