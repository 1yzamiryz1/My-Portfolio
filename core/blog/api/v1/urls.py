from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    PostViewSet,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
)

app_name = "api-v1"

router = DefaultRouter()

router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"posts", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "posts/<int:pid>/comments/",
        CommentListCreateAPIView.as_view(),
        name="post-comments",
    ),
    path(
        "comments/<int:pk>/",
        CommentRetrieveUpdateDestroyAPIView.as_view(),
        name="comment-detail",
    ),
]
