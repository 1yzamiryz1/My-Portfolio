import pytest
from django.contrib.auth.models import User
from django.urls import reverse


@pytest.mark.django_db
def test_login_view(client):
    url = reverse("accounts:login")
    response = client.get(url)
    assert (
        response.status_code == 200
    )  # Check if the view returns a 200 status code


@pytest.mark.django_db
def test_logout_view(client):
    # Create a test user
    test_user = User.objects.create_user(
        username="testuser", password="password"
    )
    client.force_login(test_user)  # Log in the test user
    url = reverse("accounts:logout")
    response = client.get(url)
    assert (
        response.status_code == 302
    )  # Check if the view redirects (302 status code)


@pytest.mark.django_db
def test_signup_view(client):
    url = reverse("accounts:signup")
    response = client.get(url)
    assert (
        response.status_code == 200
    )  # Check if the view returns a 200 status code
