from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """
    A form that extends the default UserCreationForm to include an email field.

    Attributes:
            email (EmailField): The email field for the user's email address.
    """

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Username or Email", max_length=254)

    def clean_username(self):
        username = self.cleaned_data["username"]
        return username
