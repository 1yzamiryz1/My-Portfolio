from blog.models import Post
from django.contrib.sitemaps import Sitemap
from django.utils import timezone


class BlogSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.5

    def items(self):
        return Post.objects.filter(
            status=True, published_date__lte=timezone.now()
        )

    def lastmod(self, obj):
        return obj.published_date
