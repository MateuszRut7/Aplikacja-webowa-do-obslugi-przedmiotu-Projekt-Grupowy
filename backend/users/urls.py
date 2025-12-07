from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppUserViewSet, current_user, lecturers_list  # DODAJ lecturers_list

router = DefaultRouter()
router.register('users', AppUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', current_user, name='current-user'),
    path('lecturers/', lecturers_list, name='lecturers-list'),  # DODAJ TEN WPIS
]
