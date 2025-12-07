from django.db import models
from groups.models import Group
from django.contrib.auth.models import AbstractUser


class AppUser(AbstractUser):
    numer_index = models.CharField(max_length=6, unique=True, null=True, blank=True)
    student_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)
