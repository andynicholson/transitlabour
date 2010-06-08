from django.contrib.syndication.feeds import Feed
from transitlabourapp.models import Blog

class LatestEntries(Feed):
    title = "Transit Labour latest blog entries"
    link = "http://transitlabour.asia/blog/"
    description = "Updates on the latest postings at the Transit Labour project web site."

    def items(self):
        return Blog.objects.all().order_by('-published_date')[:10]

