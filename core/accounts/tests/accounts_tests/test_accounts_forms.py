import pytest
from accounts.forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_custom_user_creation_form_valid():
    form_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password1": "testpassword123",
        "password2": "testpassword123",
    }
    form = CustomUserCreationForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_custom_user_creation_form_invalid():
    form_data = {
        "username": "testuser",
        "email": "invalidemail",
        "password1": "testpassword123",
        "password2": "testpassword123",
    }
    form = CustomUserCreationForm(data=form_data)
    assert not form.is_valid()


@pytest.mark.django_db
def test_custom_authentication_form_valid():
    User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )
    form_data = {
        "username": "testuser",
        "password": "testpassword123",
    }
    form = CustomAuthenticationForm(data=form_data)
    assert form.is_valid()


@pytest.mark.django_db
def test_custom_authentication_form_invalid():
    User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpassword123",
    )
    form_data = {
        "username": "testuser",
        "password": "wrongpassword",
    }
    form = CustomAuthenticationForm(data=form_data)
    assert not form.is_valid()
