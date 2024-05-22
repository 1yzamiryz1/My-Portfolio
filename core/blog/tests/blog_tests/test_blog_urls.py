import pytest
from blog.models import Post
from blog.views import (
    BlogListView,
    BlogSingleView,
    BlogCategoryView,
    BlogSearchView,
)
from django.urls import reverse, resolve


@pytest.mark.django_db
class TestBlogUrls:
    def test_blog_view(self, client):
        url = reverse("blog:blog_view")
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogListView

    def test_single_view(self, client):
        blog_post = Post.objects.create(
            title="Test Post", content="Test Content"
        )
        url = reverse("blog:single", kwargs={"pk": blog_post.pk})
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogSingleView

    def test_category_view(self, client):
        url = reverse(
            "blog:category", kwargs={"cat_name": "test-category"}
        )
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogCategoryView

    def test_tag_list_view(self, client):
        url = reverse("blog:tag_list", kwargs={"tag_name": "test-tag"})
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogListView

    def test_author_list_view(self, client):
        url = reverse(
            "blog:author_list", kwargs={"author_username": "test-user"}
        )
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogListView

    def test_search_view(self, client):
        url = reverse("blog:search")
        response = client.get(url)
        assert response.status_code == 200
        assert resolve(url).func.view_class == BlogSearchView
