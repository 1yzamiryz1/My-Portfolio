import requests
from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from main.models import Contact, Certificate, Project
from rest_framework import viewsets, filters, permissions

from .serializers import (
    ContactSerializer,
    CertificateSerializer,
    ProjectSerializer,
)


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "email", "subject", "message"]
    ordering_fields = ["created_date", "updated_date"]
    ordering = ["-created_date"]


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "type"]
    ordering_fields = ["created_date", "updated_date"]
    ordering = ["-created_date"]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "type"]
    ordering_fields = ["created_date", "updated_date"]
    ordering = ["-created_date"]


@cache_page(60 * 20)
def get_weather(request):
    url = (
        "https://api.open-meteo.com/v1/forecast?"
        + "latitude=35.6944&"
        + "longitude=51.4215&"
        + "hourly=temperature_2m"
    )

    response = requests.get(url)
    return JsonResponse(response.json())
