import pytest
from blog.api.v1.views import (
    CategoryViewSet,
    PostViewSet,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
)
from blog.models import Category, Post, Comment
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from rest_framework.test import APIClient
from django.utils.timezone import now


@pytest.mark.django_db
class TestURLPatterns:

    def test_category_list_url(self):
        url = reverse("blog:api-v1:category-list")
        assert resolve(url).view_name == "blog:api-v1:category-list"
        assert resolve(url).func.cls == CategoryViewSet

    def test_post_list_url(self):
        url = reverse("blog:api-v1:post-list")
        assert resolve(url).view_name == "blog:api-v1:post-list"
        assert resolve(url).func.cls == PostViewSet

    def test_post_comments_url(self):
        url = reverse("blog:api-v1:post-comments", kwargs={"pid": 1})
        assert resolve(url).view_name == "blog:api-v1:post-comments"
        assert resolve(url).func.view_class == CommentListCreateAPIView

    def test_comment_detail_url(self):
        url = reverse("blog:api-v1:comment-detail", kwargs={"pk": 1})
        assert resolve(url).view_name == "blog:api-v1:comment-detail"
        assert (
            resolve(url).func.view_class
            == CommentRetrieveUpdateDestroyAPIView
        )


@pytest.mark.django_db
class TestAPIEndpoints:

    @pytest.fixture(autouse=True)
    def setup_method(self, db):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="password"
        )

        # Create a category
        self.category = Category.objects.create(name="Test Category")

        # Create a post
        self.post = Post.objects.create(
            image="blog/default.jpg",
            author=self.user,
            title="Test Post",
            content="This is a test post.",
            counted_views=0,
            status=True,
            published_date=now(),
            login_require=False,
        )
        self.post.category.add(self.category)

        # Create a comment
        self.comment = Comment.objects.create(
            post=self.post,
            name="Test Commenter",
            email="commenter@example.com",
            subject="Test Subject",
            message="This is a test comment.",
            approved=True,
        )
        self.client = APIClient()

    def test_get_categories(self):
        response = self.client.get(reverse("blog:api-v1:category-list"))
        assert response.status_code == 200

    def test_get_posts(self):
        response = self.client.get(reverse("blog:api-v1:post-list"))
        assert response.status_code == 200

    def test_get_post_comments(self):
        response = self.client.get(
            reverse(
                "blog:api-v1:post-comments", kwargs={"pid": self.post.id}
            )
        )
        assert response.status_code == 200

    def test_get_comment_detail(self):
        response = self.client.get(
            reverse(
                "blog:api-v1:comment-detail",
                kwargs={"pk": self.comment.id},
            )
        )
        assert response.status_code == 200
