from captcha.fields import CaptchaField
from django import forms

from main.models import Contact


class ContactForm(forms.ModelForm):
    """
    A form for creating or updating contact information.

    This form includes a CaptchaField to prevent automated submissions.

    Attributes:
            captcha (CaptchaField): A field to validate user input as human.
    """

    captcha = CaptchaField()

    class Meta:
        model = Contact
        fields = ["name", "email", "subject", "message"]
