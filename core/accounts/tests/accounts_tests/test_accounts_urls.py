import pytest
from accounts import views
from django.contrib.auth import views as auth_views
from django.urls import reverse, resolve


@pytest.mark.django_db
def test_login_url():
    url = reverse("accounts:login")
    assert resolve(url).func.view_class == views.LoginView


@pytest.mark.django_db
def test_logout_url():
    url = reverse("accounts:logout")
    assert resolve(url).func.view_class == views.LogoutView


@pytest.mark.django_db
def test_signup_url():
    url = reverse("accounts:signup")
    assert resolve(url).func.view_class == views.SignupView


@pytest.mark.django_db
def test_password_reset_url():
    url = reverse("accounts:password_reset")
    assert resolve(url).func.view_class == auth_views.PasswordResetView


@pytest.mark.django_db
def test_password_reset_done_url():
    url = reverse("accounts:password_reset_done")
    assert resolve(url).func.view_class == auth_views.PasswordResetDoneView


@pytest.mark.django_db
def test_password_reset_confirm_url():
    url = reverse(
        "accounts:password_reset_confirm",
        kwargs={"uidb64": "test", "token": "test-token"},
    )
    assert (
        resolve(url).func.view_class == auth_views.PasswordResetConfirmView
    )


@pytest.mark.django_db
def test_password_reset_complete_url():
    url = reverse("accounts:password_reset_complete")
    assert (
        resolve(url).func.view_class
        == auth_views.PasswordResetCompleteView
    )
