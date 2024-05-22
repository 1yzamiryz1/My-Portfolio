from blog.models import Post, Category, Comment
from django import template

register = template.Library()


@register.filter
def snippet(value, arg=20):
    return value[:arg] + "..."


@register.inclusion_tag("blog/blog-latest-posts.html")
def latestposts(arg=3):
    posts = Post.objects.filter(status=1).order_by("-published_date")[:arg]
    return {"posts": posts}


@register.inclusion_tag("blog/blog-popular-posts.html")
def popularposts(arg=3):
    posts = Post.objects.filter(status=1).order_by("-counted_views")[:arg]
    return {"posts": posts}


@register.inclusion_tag("blog/blog-post-categories.html")
def postcategories():
    posts = Post.objects.filter(status=1)
    categories = Category.objects.all()
    cat_dict = {}
    for name in categories:
        cat_dict[name] = posts.filter(category=name).count
    return {"categories": cat_dict}


@register.simple_tag(name="comments_count")
def function(pid):
    return Comment.objects.filter(post=pid, approved=True).count()
