from .models import AppUser
from rest_framework import serializers


class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'username', 'numer_index', 'student_group', 'is_staff']  # DODAJ is_staff