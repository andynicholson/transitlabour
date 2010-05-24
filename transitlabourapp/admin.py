from django.contrib import admin
from django.http import HttpResponseRedirect

from tinymce.widgets import TinyMCE 
from transitlabour.transitlabourapp.models import Page, Blog, Event

class PageAdmin(admin.ModelAdmin):
   list_display = ('header','published_date','parent')
   search_fields = ('header',)
   list_filter = ('header', )
   prepopulated_fields = {"slug": ("header",)}

   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'teaser_text' or db_field.name=='body':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(PageAdmin, self).formfield_for_dbfield(db_field, **kwargs)
   def response_change(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_saveasnew'):
                return HttpResponseRedirect("%s" % obj.get_absolute_url())
        else:
                return super(PageAdmin,self).response_change(request,obj)

   def response_add(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
                return HttpResponseRedirect("%s" % obj.get_absolute_url())
        else:
                return super(PageAdmin,self).response_add(request,obj)

class BlogAdmin(admin.ModelAdmin):
   list_display = ('header','published_date')
   search_fields = ('header',)
   list_filter = ('header', )
   prepopulated_fields = {"slug": ("header",)}

   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'teaser_text' or db_field.name=='body':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(BlogAdmin, self).formfield_for_dbfield(db_field, **kwargs)
   def response_change(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_saveasnew'):
                return HttpResponseRedirect("/blogs/%s" % obj.get_absolute_url())
        else:
                return super(BlogAdmin,self).response_change(request,obj)

   def response_add(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
                return HttpResponseRedirect("/blogs/%s" % obj.get_absolute_url())
        else:
                return super(BlogAdmin,self).response_add(request,obj)

class EventAdmin(admin.ModelAdmin):
   list_display = ('header','published_date')
   search_fields = ('header',)
   list_filter = ('header', )
   prepopulated_fields = {"slug": ("header",)}

   def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'teaser_text' or db_field.name=='body':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                ))
        return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)
   def response_change(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue') and not request.POST.has_key('_saveasnew'):
                return HttpResponseRedirect("/events/%s" % obj.get_absolute_url())
        else:
                return super(EventAdmin,self).response_change(request,obj)

   def response_add(self, request, obj):
        if not request.POST.has_key('_addanother') and not request.POST.has_key('_continue'):
                return HttpResponseRedirect("/events/%s" % obj.get_absolute_url())
        else:
                return super(EventAdmin,self).response_add(request,obj)



admin.site.register(Event,EventAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(Page,PageAdmin)
