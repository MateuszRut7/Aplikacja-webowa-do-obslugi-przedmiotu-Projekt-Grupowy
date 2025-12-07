from django.db import models

class Topic(models.Model):
    name_topic = models.CharField(max_length=60, unique=True)  # ZMIENIONE: 30 → 60
    descriprion = models.CharField(max_length=300)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name_topic
    
    class Meta:
        ordering = ['name_topic']
