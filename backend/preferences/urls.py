from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PreferenceViewSet

router = DefaultRouter()
router.register('preferences', PreferenceViewSet)

urlpatterns = [
    path('', include(router.urls))
]