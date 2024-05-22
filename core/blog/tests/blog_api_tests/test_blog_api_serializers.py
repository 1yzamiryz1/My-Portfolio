import pytest
from blog.models import Post, Category, Comment
from blog.api.v1.serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
)
from django.contrib.auth.models import User


@pytest.fixture
def sample_category(django_db_setup):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def sample_post(sample_category, django_db_setup):
    return Post.objects.create(
        author=User.objects.create(username="test_author"),
        title="Test Post",
        content="Test Content",
        status=True,
        login_require=False,
    )


@pytest.fixture
def sample_comment(sample_post, django_db_setup):
    return Comment.objects.create(
        post=sample_post,
        name="Test User",
        email="test@example.com",
        subject="Test Subject",
        message="Test Message",
        approved=True,
    )


@pytest.mark.django_db
def test_category_serializer():
    category = Category.objects.create(name="Test Category")
    serializer = CategorySerializer(instance=category)
    assert serializer.data == {"id": category.id, "name": "Test Category"}


@pytest.mark.django_db
def test_post_serializer(sample_post, sample_category):
    sample_post.category.add(sample_category)
    serializer = PostSerializer(instance=sample_post)
    expected_data = {
        "id": sample_post.id,
        "author": sample_post.author.id,
        "image": "/media/blog/default.jpg",
        "title": "Test Post",
        "content": "Test Content",
        "tags": [],
        "category": [sample_category.id],
        "status": True,
        "published_date": None,
        "login_require": False,
    }
    assert serializer.data == expected_data


@pytest.mark.django_db
def test_comment_serializer(sample_comment, sample_post):
    serializer = CommentSerializer(instance=sample_comment)
    expected_data = {
        "id": sample_comment.id,
        "post": sample_comment.post.id,
        "name": "Test User",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "Test Message",
        "approved": True,
    }
    assert serializer.data == expected_data
