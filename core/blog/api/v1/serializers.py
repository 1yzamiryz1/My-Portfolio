from rest_framework import serializers
from blog.models import Post, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all()
    )
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "image",
            "author",
            "title",
            "content",
            "tags",
            "category",
            "status",
            "published_date",
            "login_require",
        ]

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            "id",
            "post",
            "name",
            "email",
            "subject",
            "message",
            "approved",
        ]
