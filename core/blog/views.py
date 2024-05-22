from blog.forms import CommentForm
from blog.models import Post, Comment
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin


class BlogListView(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 2

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(status=1, published_date__lte=timezone.now())
        )
        cat_name = self.kwargs.get("cat_name")
        author_username = self.kwargs.get("author_username")
        tag_name = self.kwargs.get("tag_name")
        if cat_name:
            queryset = queryset.filter(category__name=cat_name)
        if author_username:
            queryset = queryset.filter(author__username=author_username)
        if tag_name:
            queryset = queryset.filter(tags__name=tag_name)
        return queryset


class BlogSingleView(FormMixin, DetailView):
    model = Post
    template_name = "blog/blog-single.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_post = self.object
        if (
            not current_post.login_require
            or self.request.user.is_authenticated
        ):
            context["comments"] = Comment.objects.filter(
                post=current_post.id, approved=True
            )
            context["form"] = self.get_form()
            current_post.counted_views += 1
            current_post.save()
        else:
            return redirect("accounts:login")
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.post = self.object
        comment.save()
        messages.success(
            self.request, "Your Comment Submitted Successfully"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Your Comment Didnt Submitted")
        return super().form_invalid(form)


class BlogCategoryView(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        cat_name = self.kwargs.get("cat_name")
        return (
            super()
            .get_queryset()
            .filter(
                status=1,
                published_date__lte=timezone.now(),
                category__name=cat_name,
            )
        )


class BlogSearchView(ListView):
    model = Post
    template_name = "blog/blog-home.html"
    context_object_name = "posts"
    paginate_by = 3

    def get_queryset(self):
        queryset = (
            super()
            .get_queryset()
            .filter(status=1, published_date__lte=timezone.now())
        )
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(content__contains=search_query)
                | Q(title__contains=search_query)
            )
        return queryset
