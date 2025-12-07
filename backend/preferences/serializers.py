from rest_framework import serializers
from .models import Preference
from groups.models import Group
from topics.models import Topic

class PreferenceSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(source='group.name_group', read_only=True)
    topic_name = serializers.CharField(source='topic.name_topic', read_only=True)
    
    class Meta:
        model = Preference
        fields = ['id', 'group', 'group_name', 'topic', 'topic_name', 'priority', 'created_at']
        read_only_fields = ['created_at']

class PreferenceCreateSerializer(serializers.Serializer):
    """
    Serializer do tworzenia 3 preferencji na raz
    """
    group_id = serializers.IntegerField()
    preferences = serializers.ListField(
        child=serializers.DictField(
            child=serializers.IntegerField()
        )
    )
    
    def validate(self, data):
        # Sprawdź czy grupa istnieje
        if not Group.objects.filter(id=data['group_id']).exists():
            raise serializers.ValidationError("Grupa nie istnieje")
        
        # Sprawdź czy są dokładnie 3 preferencje
        if len(data['preferences']) != 3:
            raise serializers.ValidationError("Musisz podać dokładnie 3 preferencje")
        
        # Sprawdź priorytety 1,2,3
        priorities = [p['priority'] for p in data['preferences']]
        if sorted(priorities) != [1, 2, 3]:
            raise serializers.ValidationError("Priorytety muszą być 1, 2 i 3")
        
        return data