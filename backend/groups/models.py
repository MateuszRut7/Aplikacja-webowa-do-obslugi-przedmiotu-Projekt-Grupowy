from django.db import models
from topics.models import Topic
import string
import random


# Create your models here.
class Group(models.Model):
    name_group = models.CharField(max_length=30, unique=True)
    lecturer = models.ForeignKey('users.AppUser', on_delete=models.CASCADE, null=True)
    topic = models.OneToOneField(Topic, on_delete=models.CASCADE, null=True)
    code = models.CharField(max_length=30, unique=True, null=True)

    def save(self, *args, **kwargs):
        password = ''
        for i in range(6):
            chars = string.digits
            password = password + random.choice(chars)
        self.code = password
        super().save(*args, **kwargs)
