from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from .models import Preference
from .serializers import PreferenceSerializer, PreferenceCreateSerializer
from groups.models import Group
from topics.models import Topic

class PreferenceViewSet(viewsets.ModelViewSet):
    queryset = Preference.objects.all()
    serializer_class = PreferenceSerializer
    
    @list_route(methods=['POST'], url_path='save-preferences')
    def save_preferences(self, request, *args, **kwargs):
        """
        Zapisz 3 preferencje dla grupy
        """
        serializer = PreferenceCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        data = serializer.validated_data
        group_id = data['group_id']
        preferences_data = data['preferences']
        
        try:
            group = Group.objects.get(id=group_id)
            
            # Usuń stare preferencje tej grupy
            Preference.objects.filter(group=group).delete()
            
            # Stwórz nowe preferencje
            created_preferences = []
            for pref_data in preferences_data:
                topic = Topic.objects.get(id=pref_data['topic_id'])
                preference = Preference.objects.create(
                    group=group,
                    topic=topic,
                    priority=pref_data['priority']
                )
                created_preferences.append(preference)
            
            # Zwróć utworzone preferencje
            result_serializer = PreferenceSerializer(created_preferences, many=True)
            return Response({
                'message': 'Preferencje zapisane pomyślnie',
                'preferences': result_serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Group.DoesNotExist:
            return Response({'error': 'Grupa nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
        except Topic.DoesNotExist:
            return Response({'error': 'Jeden z tematów nie istnieje'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @list_route(methods=['GET'], url_path='group-preferences')
    def get_group_preferences(self, request, *args, **kwargs):
        """
        Pobierz preferencje danej grupy
        """
        group_id = request.query_params.get('group_id')
        if not group_id:
            return Response({'error': 'Podaj group_id'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            group = Group.objects.get(id=group_id)
            preferences = Preference.objects.filter(group=group).order_by('priority')
            serializer = PreferenceSerializer(preferences, many=True)
            return Response(serializer.data)
        except Group.DoesNotExist:
            return Response({'error': 'Grupa nie istnieje'}, status=status.HTTP_404_NOT_FOUND)