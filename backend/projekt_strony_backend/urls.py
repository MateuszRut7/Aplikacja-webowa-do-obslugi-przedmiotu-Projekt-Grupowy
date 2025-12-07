"""projekt_strony_frontend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from .signals import Permissions
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api/groups/', include('groups.urls')),
    path(r'api/users/', include('users.urls')),
    path(r'api/topics/', include('topics.urls')),
    path(r'api/preferences/', include('preferences.urls')),  # DODAJ TUTAJ
    path(r'api/permissions/', Permissions.as_view()),
    path(r'api/login/', obtain_auth_token, name='login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)