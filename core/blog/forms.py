from blog.models import Comment
from django import forms


class CommentForm(forms.ModelForm):
    """
    A form for adding comments to a blog post.

    This form allows users to submit comments with their name, email,
    subject, and message.

    Attributes:
            name (CharField): The name of the commenter.
            email (EmailField): The email address of the commenter.
            subject (CharField): The subject of the comment.
            message (CharField): The content of the comment.
    """

    class Meta:
        model = Comment
        fields = ["name", "email", "subject", "message"]
