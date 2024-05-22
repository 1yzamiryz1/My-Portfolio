from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import (
    ContactViewSet,
    CertificateViewSet,
    ProjectViewSet,
    get_weather,
)

app_name = "api-v1"

router = DefaultRouter()
router.register(r"contacts", ContactViewSet, basename="contact")
router.register(
    r"certificates", CertificateViewSet, basename="certificate"
)
router.register(r"projects", ProjectViewSet, basename="project")


urlpatterns = [
    path("", include(router.urls)),
    path("get-weather/", get_weather, name="get_weather"),
]
