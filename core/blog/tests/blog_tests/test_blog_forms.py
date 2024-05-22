import pytest
from blog.forms import CommentForm


@pytest.mark.django_db
def test_comment_form_valid_data():
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Test Subject",
        "message": "This is a test message.",
    }
    form = CommentForm(data=form_data)
    assert form.is_valid(), "Form should be valid with correct data"


@pytest.mark.django_db
def test_comment_form_missing_name():
    form_data = {
        "email": "john@example.com",
        "subject": "Test Subject",
        "message": "This is a test message.",
    }
    form = CommentForm(data=form_data)
    assert not form.is_valid(), "Form should be invalid without a name"
    assert "name" in form.errors, "Name field should have an error"


@pytest.mark.django_db
def test_comment_form_invalid_email():
    form_data = {
        "name": "John Doe",
        "email": "invalid-email",
        "subject": "Test Subject",
        "message": "This is a test message.",
    }
    form = CommentForm(data=form_data)
    assert (
        not form.is_valid()
    ), "Form should be invalid with an incorrect email format"
    assert "email" in form.errors, "Email field should have an error"


@pytest.mark.django_db
def test_comment_form_missing_message():
    form_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "subject": "Test Subject",
    }
    form = CommentForm(data=form_data)
    assert not form.is_valid(), "Form should be invalid without a message"
    assert "message" in form.errors, "Message field should have an error"
