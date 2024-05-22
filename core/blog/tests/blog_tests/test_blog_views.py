import pytest
from blog.models import Post, Category, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone


@pytest.fixture
def user(db):
    return User.objects.create_user(username="testuser", password="12345")


@pytest.fixture
def category(db):
    return Category.objects.create(name="Django")


@pytest.fixture
def post(db, user, category):
    post = Post.objects.create(
        author=user,
        title="Test Post",
        content="This is a test post",
        status=True,
        published_date=timezone.now(),
        login_require=False,
    )
    post.category.set([category])
    return post


@pytest.fixture
def client_logged_in(client, user):
    client.login(username="testuser", password="12345")
    return client


def test_blog_list_view(client, post):
    url = reverse("blog:blog_view")
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context
    assert post in response.context["posts"]


def test_blog_single_view(client, post):
    url = reverse("blog:single", kwargs={"pk": post.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "post" in response.context
    assert response.context["post"] == post


def test_blog_single_view_with_comments(client, post):
    comment = Comment.objects.create(
        post=post,
        name="Test User",
        email="test@example.com",
        subject="Test Subject",
        message="Test message",
        approved=True,
    )
    url = reverse("blog:single", kwargs={"pk": post.id})
    response = client.get(url)
    assert response.status_code == 200
    assert "comments" in response.context
    assert comment in response.context["comments"]


def test_blog_category_view(client, category, post):
    url = reverse("blog:category", kwargs={"cat_name": category.name})
    response = client.get(url)
    assert response.status_code == 200
    assert "posts" in response.context
    assert post in response.context["posts"]


def test_blog_search_view(client, post):
    url = reverse("blog:search")
    response = client.get(url, {"search": "test"})
    assert response.status_code == 200
    assert "posts" in response.context
    assert post in response.context["posts"]


def test_blog_single_view_with_authenticated_user(client_logged_in, post):
    post.login_require = True
    post.save()
    url = reverse("blog:single", kwargs={"pk": post.id})
    response = client_logged_in.get(url)
    assert response.status_code == 200
    assert "post" in response.context
    assert response.context["post"] == post
