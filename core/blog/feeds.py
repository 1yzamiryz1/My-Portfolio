from blog.models import Post
from django.contrib.syndication.views import Feed
from django.utils import timezone


class LatestEntriesFeed(Feed):
    title = "Blog newest posts"
    link = "/rss/feed"
    description = "Best blog ever."

    def items(self):
        return Post.objects.filter(
            status=True, published_date__lte=timezone.now()
        )

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content[:100]
