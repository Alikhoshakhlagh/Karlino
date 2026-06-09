"""
URL configuration for karlino project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth_api.urls')),
    path('api/company/', include('apps.companies.urls')),
    path('api/projects/', include('apps.projects.urls')),
    path('api/applications/', include('apps.applications.urls')),
    path('api/favorites/', include('apps.favorites.urls')),
    path('api/categories/', include('apps.categories.urls')),
    path('api/skills/', include('apps.skills.urls')),

    #swagger
    path('api/schema/',SpectacularAPIView.as_view(),name='schema',),
    path('api/docs/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui',),
    path('api/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc',),
    
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
