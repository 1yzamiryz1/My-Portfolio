import re

from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect
from django.shortcuts import render, reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView
from django.views.generic.edit import FormView

from .forms import CustomAuthenticationForm
from .forms import CustomUserCreationForm


class LoginView(View):
    form_class = CustomAuthenticationForm
    template_name = "accounts/login.html"

    def is_valid_email(self, email):
        email_regex = (
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        return re.match(email_regex, email)

    def email_to_username(self, email):
        try:
            user = User.objects.get(email=email)
            return user.username
        except User.DoesNotExist:
            return None

    def get(self, request):
        if not request.user.is_authenticated:
            form = self.form_class()
            context = {"form": form}
            return render(request, self.template_name, context)
        else:
            return redirect(reverse("main:index_view"))

    def post(self, request):
        if not request.user.is_authenticated:
            form = self.form_class(
                request=request, data=request.POST.copy()
            )
            login_data = form.data.get("username")
            is_email = self.is_valid_email(login_data)

            if is_email:
                username_from_email = self.email_to_username(login_data)
                if username_from_email:
                    form.data["username"] = username_from_email

            if form.is_valid():
                login_data = form.cleaned_data.get("username")
                password = form.cleaned_data.get("password")
                user = authenticate(
                    request, username=login_data, password=password
                )

                if user is not None:
                    login(request, user)
                    messages.add_message(
                        request,
                        messages.SUCCESS,
                        f"{login_data} logged in successfully",
                    )
                    return redirect(reverse("main:index_view"))
                else:
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Sorry, we couldn't log you in",
                    )
                    return redirect(reverse("main:index_view"))
            else:
                context = {"form": form}
                return render(request, self.template_name, context)
        else:
            return redirect(reverse("main:index_view"))


class LogoutView(LoginRequiredMixin, RedirectView):
    """
    Handles user logout functionality.
    """

    pattern_name = "main:index_view"

    def get_redirect_url(self, *args, **kwargs):
        logout(self.request)
        messages.success(self.request, "Logged Out Successfully")
        return super().get_redirect_url(*args, **kwargs)


class SignupView(FormView):
    """
    Handles user signup functionality.
    """

    template_name = "accounts/signup.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("accounts:login")

    def is_user_exists(self, email, username):
        User = get_user_model()
        return (
            User.objects.filter(email=email).exists()
            or User.objects.filter(username=username).exists()
        )

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        username = form.cleaned_data.get("username")

        if self.is_user_exists(email, username):
            messages.error(
                self.request, "This email or username is already in use."
            )
            return self.form_invalid(form)

        form.save()
        messages.success(self.request, "User created Successfully")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Sorry Something went wrong")
        return super().form_invalid(form)


def is_user_exists(email, username):
    """
    Checks if a user with the given email or username already exists.

    Args:
        email (str): The email address to check.
        username (str): The username to check.

    Returns:
        bool: True if a user with the given email or username exists,
        False otherwise.
    """
    return User.objects.filter(
        Q(email=email) | Q(username=username)
    ).exists()
