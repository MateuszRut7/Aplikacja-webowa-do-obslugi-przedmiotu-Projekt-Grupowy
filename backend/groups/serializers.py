from .models import Group
from rest_framework import serializers
from users.models import AppUser
from topics.models import Topic


class GroupSerializer(serializers.ModelSerializer):
    # Pola ForeignKey - używamy CharField aby obsłużyć różne formaty
    lecturer = serializers.CharField(required=False, allow_null=True)
    topic = serializers.PrimaryKeyRelatedField(
        queryset=Topic.objects.all(),
        required=False,
        allow_null=True
    )
    
    # Pola tylko do odczytu dla wyświetlania
    lecturer_display = serializers.SerializerMethodField()
    topic_display = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name_group', 'code', 'lecturer', 'topic', 'lecturer_display', 'topic_display']
        read_only_fields = ('code',)

    def get_lecturer_display(self, obj):
        if obj.lecturer:
            return {
                'id': obj.lecturer.id,
                'username': obj.lecturer.username,
                'first_name': obj.lecturer.first_name,
                'last_name': obj.lecturer.last_name
            }
        return None

    def get_topic_display(self, obj):
        if obj.topic:
            return {
                'id': obj.topic.id,
                'name_topic': obj.topic.name_topic,
                'description': obj.topic.descriprion
            }
        return None

    def validate_lecturer(self, value):
        """Konwertuj lecturer (może być ID lub username) na obiekt AppUser"""
        if value is None or value == '':
            return None
        
        try:
            # Jeśli value to liczba (ID)
            if isinstance(value, (int, str)) and value.isdigit():
                lecturer = AppUser.objects.get(id=int(value), is_staff=True)
                return lecturer
            # Jeśli value to string (username)
            elif isinstance(value, str):
                lecturer = AppUser.objects.get(username=value, is_staff=True)
                return lecturer
        except AppUser.DoesNotExist:
            raise serializers.ValidationError(f"Wykładowca '{value}' nie istnieje lub nie jest wykładowcą")
        except ValueError:
            raise serializers.ValidationError(f"Nieprawidłowa wartość dla wykładowcy: {value}")
        
        raise serializers.ValidationError(f"Nieznany format danych wykładowcy: {value}")

    def validate_topic(self, value):
        """Upewnij się, że topic jest prawidłowy"""
        if value is None:
            return None
        return value  # PrimaryKeyRelatedField już to waliduje

    def create(self, validated_data):
        # Wyciągnij lecturer z validated_data (już zwalidowany jako obiekt)
        lecturer = validated_data.pop('lecturer', None)
        
        # Utwórz grupę
        group = Group.objects.create(**validated_data)
        
        # Ustaw lecturer jeśli został podany
        if lecturer:
            group.lecturer = lecturer
            group.save()
        
        return group

    def update(self, instance, validated_data):
        # Wyciągnij lecturer z validated_data (już zwalidowany jako obiekt)
        lecturer = validated_data.pop('lecturer', None)
        
        # Zaktualizuj podstawowe pola
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        # Ustaw lecturer jeśli został podany
        if lecturer is not None:  # Uwaga: None oznacza "usuń prowadzącego"
            instance.lecturer = lecturer
        
        instance.save()
        return instance
