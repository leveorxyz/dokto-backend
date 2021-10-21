"""Dokto_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import debug_toolbar
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny

from .views import Custom404


schema_view = get_schema_view(
    openapi.Info(
        title="Dokto API",
        default_version=settings.VERSION,
        description="Dokto API",
    ),
    public=True,
    permission_classes=(AllowAny,),
)

urlpatterns = [
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
    path("admin/", admin.site.urls),
    path("accounting/", include("accounting.urls")),
    path("user/", include("user.urls")),
    path("docs/", include_docs_urls(title="Dokto API")),
    path("__debug__/", include(debug_toolbar.urls)),
    url(
        r"^media/(?P<path>.*)$",
        serve,
        {"document_root": settings.MEDIA_ROOT, "show_indexes": True},
    ),
]

urlpatterns += staticfiles_urlpatterns()

handler404 = Custom404.as_view()
