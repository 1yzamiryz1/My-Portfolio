from blog.feeds import LatestEntriesFeed
from blog.views import (
    BlogListView,
    BlogSingleView,
    BlogCategoryView,
    BlogSearchView,
)
from django.urls import path, include

app_name = "blog"

urlpatterns = [
    path("", BlogListView.as_view(), name="blog_view"),
    path("<int:pk>/", BlogSingleView.as_view(), name="single"),
    path(
        "category/<str:cat_name>/",
        BlogCategoryView.as_view(),
        name="category",
    ),
    path("tag/<str:tag_name>/", BlogListView.as_view(), name="tag_list"),
    path(
        "author/<str:author_username>/",
        BlogListView.as_view(),
        name="author_list",
    ),
    path("search/", BlogSearchView.as_view(), name="search"),
    path("rss/feed/", LatestEntriesFeed(), name="rss_feed"),
    path("api/v1/", include("blog.api.v1.urls")),
]
