
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
from solango.views import SearchView
import datetime

OBJECTS_PER_PAGE = 4

def is_owner_of(request, obj):

	if request.user.is_superuser:
		return True
	if request.user.is_authenticated and obj.author == request.user:
		return True
	return False

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
	template_file_name='home'
	page_name=platform_name

	platform = Platform.objects.all().filter(name=platform_name)

	blogs = Blog.objects.all().filter(promoted_platform=True, platform=platform).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted_platform=False, platform=platform).order_by('-published_date')

	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('starting_date')[:5]

	bloggers = latest_bloggers(lblogs)

   	#paginate results
        blog_paginator = paginate(request,lblogs)
	page_set = Page.objects.filter(slug=page_name)

	extra_context = {'bloggers':bloggers, 'pblogs':blogs, 'lblogs':blog_paginator, 'events':events , 'platformpage':True, 'is_page_owner': is_owner_of(request,page_set[0]) }

	# find the page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def home_view(request):
	#find the required blog via its slug 'slug_name'
	template_file_name='home'
	page_name='home'

	blogs = Blog.objects.all().filter(promoted=True).order_by('-published_date')[:2]
        lblogs = Blog.objects.all().filter(promoted=False).order_by('-published_date')
	today = datetime.datetime.today()
	events = Event.objects.all().filter(ending_date__gt=today).order_by('starting_date')[:5]

	#paginate results
	blog_paginator = paginate(request,lblogs)

	hp = Page.objects.filter(slug=page_name)
	extra_context = {'pblogs':blogs, 'lblogs':blog_paginator, 'events':events , 'homepage':True, 'is_page_owner': is_owner_of(request,hp[0]) }

	# find the page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = hp, slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def blog_view(request, slug_name, author_name):
	# note - this is currently only used for a specfic blog view and author view - not the front page of the "blogs" section of the site
	# check urls.py carefully
	is_owner = False

	#find the required blog via its slug 'slug_name'
	if not slug_name is None:
		blogs = Blog.objects.all().filter(slug=slug_name).order_by('-published_date')
		author_view = False
		blog_view = True
		bauthor = None
		sticky_blogs = None
		is_owner = is_owner_of(request, blogs[0])
	else:
		#no slugname - author view
		bauthor = User.objects.all().filter(username=author_name)[0]
		blogs = Blog.objects.all().filter(author=bauthor, sticky=False).order_by('-published_date')
		sticky_blogs = Blog.objects.all().filter(author=bauthor, sticky=True).order_by('-published_date')
		author_view = True
		blog_view = False
	#get list of latest bloggers
	bloggers = latest_bloggers(Blog.objects.all().order_by('-published_date'))
	#paginate results
	blog_paginator = paginate(request,blogs)

	extra_context = {'bloggers':bloggers, 'blogs':blog_paginator, 'blog_view':blog_view, 'author_view':author_view, 'bauthor':bauthor, 'sticky_blogs':sticky_blogs, 'is_owner':is_owner}

	template_file_name='blogs'
	page_name='blogs'
	# find the page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def event_view(request, slug_name, author_name):
	#find the required blog via its slug 'slug_name'
	is_owner = False
	if not slug_name is None:
		events = Event.objects.all().filter(slug=slug_name).order_by('starting_date')
		author_view = False
		event_view = True
		bauthor = None
		is_owner = is_owner_of(request,events[0])
	else:
		bauthor = User.objects.all().filter(username=author_name)[0]
		events = Event.objects.all().filter(author=bauthor).order_by('starting_date')
		author_view = True
		event_view = False

	bloggers=[]
	events_paginator = paginate(request,events)

	extra_context = {'bloggers':bloggers, 'events':events_paginator, 'event_view':event_view, 'author_view':author_view, 'bauthor':bauthor, 'is_owner':is_owner}

	template_file_name='events'
	page_name='events'
	# find the page object which represents the actual page (not blogs within page) by its slug name 'page_name' , and the template
	return object_detail( request, queryset = Page.objects.filter(slug=page_name), slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )


def page_view(request, page_name):
	blogs = Blog.objects.all().order_by('-published_date')

	enddate_cutoff = datetime.date.today().isoformat()
	events = Event.objects.all().order_by('starting_date').filter(ending_date__gte = enddate_cutoff)
	past_events = Event.objects.all().order_by('-starting_date').filter(ending_date__lte = enddate_cutoff)

	bloggers = latest_bloggers(blogs)

	#paginate the blogs homepage
	blogs_paginator = paginate(request,blogs)

	#paginate the events homepage
	events_paginator = paginate(request,events)
	past_events_paginator = paginate(request,past_events)
	past_events_flag = ( len(past_events) > 0)	
	previous_events_flag = False

	if request.GET.get('previous_events',None) == 'y':
		events_paginator = past_events_paginator
		previous_events_flag = True


	page_obj = Page.objects.filter(slug=page_name)
	is_owner = is_owner_of(request, page_obj[0]) 

	extra_context = {'bloggers':bloggers, 'blogs':blogs_paginator, 'events':events_paginator ,'past_events_available':past_events_flag, 'showing_previous_events': previous_events_flag, 'is_page_owner':is_owner}

	#decide which template file to use based on page name
	# ie - this view currently handles blogs, and events top level pages, plus misc. static pages
	if page_name=='blogs' or page_name=='events':
		template_file_name=page_name
	else:
		#generic template to use for all other pages
		template_file_name='about'
	return object_detail( request, queryset = page_obj , slug=page_name, template_name="transitlabourapp/%s.html"%template_file_name, extra_context=extra_context )

def search_detail(request):
        solango_searchview = SearchView(template_name="transitlabourapp/search.html")
	blogs = Blog.objects.all().order_by('-published_date')
	bloggers = latest_bloggers(blogs)
	object = Page.objects.all().filter(slug='search')[0]

        return solango_searchview.main(request, extra_context = {"bloggers":bloggers, "object":object})



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
