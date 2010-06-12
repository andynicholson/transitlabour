import solango
from transitlabour.transitlabourapp.models import Page, Blog

class PageSearchDocument(solango.SearchDocument):
    date = solango.fields.DateField()
    header = solango.fields.CharField(copy=True)
    teaser_text = solango.fields.TextField(copy=True)
    body = solango.fields.TextField(copy=True)
    author = solango.fields.CharField(copy=True)
    slug = solango.fields.CharField(copy=True)

    class Media:
        template = 'transitlabourapp/page_searchdocument.html'

    def transform_date(self, instance):
        return instance.published_date

    def tranform_author(self,instance):
	return instance.author.first_name + ' ' + instance.author.last_name

class BlogSearchDocument(solango.SearchDocument):
    date = solango.fields.DateField()
    header = solango.fields.CharField(copy=True)
    teaser_text = solango.fields.TextField(copy=True)
    body = solango.fields.TextField(copy=True)
    author = solango.fields.CharField(copy=True)
    slug = solango.fields.CharField(copy=True)

    class Media:
        template = 'transitlabourapp/blog_searchdocument.html'

    def transform_date(self, instance):
        return instance.published_date

    def tranform_author(self,instance):
	return instance.author.first_name + ' ' + instance.author.last_name

solango.register(Page, PageSearchDocument)
solango.register(Blog, BlogSearchDocument)

