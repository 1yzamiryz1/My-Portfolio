from blog.models import Post, Category, Comment
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = (
        "id",
        "author",
        "title",
        "counted_views",
        "login_require",
        "status",
        "published_date",
        "created_date",
    )
    list_filter = ("status", "author")
    ordering = ["-created_date"]
    search_fields = ["title", "content"]
    summernote_fields = ("content",)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    date_hierarchy = "created_date"
    empty_value_display = "-empty-"
    list_display = (
        "name",
        "post",
        "approved",
        "created_date",
        "updated_date",
    )
    list_filter = ("post", "approved")
    ordering = ["-created_date"]
    search_fields = ["name", "post"]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
