import pytest
from blog.api.v1.serializers import (
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
)
from blog.models import Category, Post, Comment
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_category_view_set():
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    category_data = {"name": "Test Category"}
    response = client.post(
        reverse("blog:api-v1:category-list"), category_data, format="json"
    )
    assert response.status_code == 201

    category = Category.objects.get(name="Test Category")
    assert category.name == "Test Category"
    assert CategorySerializer(instance=category).data == response.data


@pytest.mark.django_db
def test_post_view_set():
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Test Category")

    post_data = {
        "title": "Test Post",
        "content": "Test Content",
        "category": [category.id],
    }
    response = client.post(
        reverse("blog:api-v1:post-list"), post_data, format="json"
    )
    assert response.status_code == 201

    post = Post.objects.get(title="Test Post")
    assert post.title == "Test Post"
    assert post.content == "Test Content"
    assert post.category.filter(id=category.id).exists()

    # Exclude the 'image' field from comparison
    post_data = PostSerializer(
        instance=post, context={"request": response.wsgi_request}
    ).data
    response_data = response.data
    post_data.pop("image", None)
    response_data.pop("image", None)

    assert post_data == response_data


@pytest.mark.django_db
def test_comment_list_create_api_view():
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Test Category")
    post = Post.objects.create(title="Test Post", content="Test Content")
    post.category.add(category)

    comment_data = {
        "post": post.id,
        "name": "Test Name",
        "email": "test@example.com",
        "subject": "Test Subject",
        "message": "Test Message",
    }
    response = client.post(
        reverse("blog:api-v1:post-comments", kwargs={"pid": post.id}),
        comment_data,
        format="json",
    )

    if response.status_code != 201:
        print(f"Response status code: {response.status_code}")
        print(f"Response content: {response.content}")

    assert response.status_code == 201

    comment = Comment.objects.get(message="Test Message")
    assert comment.name == "Test Name"
    assert comment.email == "test@example.com"
    assert comment.subject == "Test Subject"
    assert comment.message == "Test Message"
    assert CommentSerializer(instance=comment).data == response.data


@pytest.mark.django_db
def test_comment_retrieve_update_destroy_api_view():
    user = User.objects.create_user(
        username="test_user", password="test_password"
    )
    client = APIClient()
    client.force_authenticate(user=user)

    category = Category.objects.create(name="Test Category")
    post = Post.objects.create(title="Test Post", content="Test Content")
    post.category.add(category)
    comment = Comment.objects.create(
        post=post,
        name="Test Name",
        email="test@example.com",
        subject="Test Subject",
        message="Test Message",
    )

    response = client.get(
        reverse("blog:api-v1:comment-detail", kwargs={"pk": comment.id})
    )
    assert response.status_code == 200

    comment_data = {
        "name": "Updated Name",
        "email": "updated@example.com",
        "subject": "Updated Subject",
        "message": "Updated Message",
    }
    response = client.patch(
        reverse("blog:api-v1:comment-detail", kwargs={"pk": comment.id}),
        comment_data,
        format="json",
    )
    assert response.status_code == 200

    updated_comment = Comment.objects.get(id=comment.id)
    assert updated_comment.name == "Updated Name"
    assert updated_comment.email == "updated@example.com"
    assert updated_comment.subject == "Updated Subject"
    assert updated_comment.message == "Updated Message"
