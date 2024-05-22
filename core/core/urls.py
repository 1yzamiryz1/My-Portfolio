"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

import django.contrib.auth.urls
from blog.sitemaps import BlogSitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from main.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "blog": BlogSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("", include("main.urls", namespace="main")),
    path("blog/", include("blog.urls", namespace="blog")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("robots.txt", include("robots.urls")),
    path("summernote/", include("django_summernote.urls")),
    path("captcha/", include("captcha.urls")),
    path("", include(django.contrib.auth.urls)),
]

if settings.COMINGSOON:
    urlpatterns.insert(
        0,
        re_path(
            r"^", TemplateView.as_view(template_name="comingsoon.html")
        ),
    )

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

if settings.SHOW_DEBUGGER_TOOLBAR:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

if settings.SHOW_SWAGGER:
    urlpatterns += [
        path(
            "api-auth/",
            include("rest_framework.urls", namespace="rest_framework"),
        ),
        path("schema/", SpectacularAPIView.as_view(), name="schema"),
        path(
            "swagger/",
            SpectacularSwaggerView.as_view(url_name="schema"),
            name="swagger-ui",
        ),
    ]

handler400 = "core.error_views.error_400"  # bad_request
handler403 = "core.error_views.error_403"  # permission_denied
handler404 = "core.error_views.error_404"  # page_not_found
handler500 = "core.error_views.error_500"  # server_error
