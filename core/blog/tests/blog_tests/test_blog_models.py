import pytest
from django.contrib.auth.models import User
from django.utils import timezone
from blog.models import Category, Post, Comment


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Test Category")
    assert category.name == "Test Category"
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_post_creation():
    user = User.objects.create_user(
        username="testuser", password="password"
    )
    category = Category.objects.create(name="Test Category")
    post = Post.objects.create(
        author=user,
        title="Test Post",
        content="This is a test post.",
        counted_views=10,
        status=True,
        published_date=timezone.now(),
        login_require=True,
    )
    post.category.add(category)

    assert post.author == user
    assert post.title == "Test Post"
    assert post.content == "This is a test post."
    assert post.counted_views == 10
    assert post.status is True
    assert post.category.count() == 1
    assert category in post.category.all()
    assert post.login_require is True
    assert str(post) == "Test Post"


@pytest.mark.django_db
def test_comment_creation():
    user = User.objects.create_user(
        username="testuser", password="password"
    )
    post = Post.objects.create(
        author=user,
        title="Test Post",
        content="This is a test post.",
        counted_views=10,
        status=True,
        published_date=timezone.now(),
        login_require=True,
    )
    comment = Comment.objects.create(
        post=post,
        name="Test User",
        email="testuser@example.com",
        subject="Test Subject",
        message="This is a test comment.",
        approved=True,
    )

    assert comment.post == post
    assert comment.name == "Test User"
    assert comment.email == "testuser@example.com"
    assert comment.subject == "Test Subject"
    assert comment.message == "This is a test comment."
    assert comment.approved is True
    assert str(comment) == "Test User"
