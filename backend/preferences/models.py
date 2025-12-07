from django.db import models
from groups.models import Group
from topics.models import Topic

class Preference(models.Model):
    """
    Preferencje tematów wybrane przez grupę
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='preferences')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    priority = models.IntegerField(choices=[(1, '1 - Najwyższy'), (2, '2 - Średni'), (3, '3 - Najniższy')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = [['group', 'priority']]  # Grupa nie może mieć dwóch tematów z tym samym priorytetem
        ordering = ['group', 'priority']
    
    def __str__(self):
        return f"{self.group.name_group} - Priorytet {self.priority}: {self.topic.name_topic}"