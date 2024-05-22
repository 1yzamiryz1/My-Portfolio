from django.urls import path, include

from main.views import IndexView, AboutView, ContactView

app_name = "main"

urlpatterns = [
    path("", IndexView.as_view(), name="index_view"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("api/v1/", include("main.api.v1.urls")),
]
