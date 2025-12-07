from .models import Topic
from .serializers import TopicSerializer
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import list_route
from projekt_strony_backend.permissions import IsLecturer

class TopicViewSet(viewsets.ModelViewSet):
    # TYLKO AKTYWNE TEMATY
    queryset = Topic.objects.filter(is_active=True)
    serializer_class = TopicSerializer
    
    def get_permissions(self):
        # Pozwól wszystkim na przeglądanie (GET)
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        # Tylko wykładowcy mogą tworzyć/edygować/usuwać
        return [IsLecturer()]
    
    def get_queryset(self):
        # Dla wszystkich GET, pokazuj tylko aktywne
        if self.request.method == 'GET':
            return Topic.objects.filter(is_active=True)
        # Dla innych metod (POST, PUT, DELETE) - wykładowcy widzą wszystko
        return Topic.objects.all()
    
    def perform_destroy(self, instance):
        # Zamiast usuwać, oznacz jako nieaktywny (SOFT DELETE)
        instance.is_active = False
        instance.save()
        
        # Jeśli jakaś grupa miała przypisany ten temat, odepnij go
        from groups.models import Group
        Group.objects.filter(topic=instance).update(topic=None)
    
    # Dodatkowy endpoint do przywracania tematów (tylko dla wykładowców)
    @list_route(methods=['post'], url_path='restore/(?P<pk>[^/.]+)')
    def restore(self, request, pk=None):
        """Przywróć temat (tylko wykładowca)"""
        try:
            topic = Topic.objects.get(id=pk, is_active=False)
        except Topic.DoesNotExist:
            return Response(
                {'error': 'Temat nie istnieje lub jest już aktywny'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        topic.is_active = True
        topic.save()
        return Response({'status': 'topic restored', 'id': topic.id})
    
    # Endpoint do przeglądania usuniętych tematów (tylko dla wykładowców)
    @list_route(methods=['get'], url_path='deleted')
    def deleted_topics(self, request):
        """Pokaż usunięte tematy (tylko wykładowca)"""
        if not (request.user.groups.filter(name='lecturer').exists() or request.user.is_staff):
            return Response(
                {'detail': 'Tylko wykładowcy mogą przeglądać usunięte tematy.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        deleted_topics = Topic.objects.filter(is_active=False)
        serializer = self.get_serializer(deleted_topics, many=True)
        return Response(serializer.data)
