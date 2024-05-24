from itertools import groupby
from operator import attrgetter

from django.contrib import messages
from django.views.generic import TemplateView, FormView
from main.forms import ContactForm
from main.models import Certificate, Project


class IndexView(TemplateView):
    """View for rendering the index page."""

    template_name = "main/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        projects = Project.objects.all().order_by("-type")
        context["projects"] = projects
        return context


class AboutView(TemplateView):
    """View for rendering the about page."""

    template_name = "main/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        certificates = Certificate.objects.all().order_by("-type")

        # Define the custom sorting order
        custom_order = {
            "Django": 1,
            "Python": 2,
            "Web": 3,
            "Data": 4,
            "other": 5,
        }

        # Sort certificates by custom order
        sorted_certificates = sorted(
            certificates, key=lambda x: custom_order.get(x.type, 6)
        )

        grouped_certificates = {}
        for key, group in groupby(
            sorted_certificates, key=attrgetter("type")
        ):
            grouped_certificates[key] = list(group)
        context["grouped_certificates"] = grouped_certificates
        return context


class ContactView(FormView):
    """View for handling contact form submission and rendering contact page."""

    template_name = "main/contact.html"
    form_class = ContactForm
    success_url = "/contact/"

    def form_valid(self, form):
        form.save()
        messages.success(
            self.request, "Your ticket submitted successfully"
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Your ticket didn't submit")
        return super().form_invalid(form)
