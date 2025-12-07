from .models import Group
from .serializers import GroupSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_fields = '__all__'
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = '__all__'
    
    def get_permissions(self):
        # Tylko wykładowcy mogą usuwać grupy
        if self.action in ['destroy']:
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        # Wszyscy zalogowani mogą tworzyć/edygować/przeglądać
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        
        # Wykładowcy widzą wszystkie grupy
        if user.groups.filter(name='lecturer').exists() or user.is_staff:
            return Group.objects.all()
        
        # Studenci widzą tylko swoją grupę
        if user.student_group:
            return Group.objects.filter(id=user.student_group.id)
        
        # Jeśli student nie ma grupy, widzi pusto (ale może stworzyć)
        return Group.objects.none()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        
        user = request.user
        
        # Studenci mogą edytować TYLKO swoją grupę, ALE tylko niektóre pola
        if not (user.groups.filter(name='lecturer').exists() or user.is_staff):
            if hasattr(user, 'student_group') and user.student_group:
                if obj.id != user.student_group.id:
                    self.permission_denied(
                        request, 
                        message='Możesz edytować tylko swoją grupę.'
                    )
                else:
                    # Student może edytować tylko swoją grupę, ale nie może zmieniać:
                    # - prowadzącego (lecturer)
                    # - przypisanego tematu (topic)
                    # Tylko może zmieniać nazwę grupy
                    if 'lecturer' in request.data or 'topic' in request.data:
                        self.permission_denied(
                            request,
                            message='Student nie może zmieniać prowadzącego ani tematu grupy.'
                        )
            else:
                # Student bez grupy nie może edytować żadnej
                self.permission_denied(
                    request,
                    message='Nie masz grupy do edycji.'
                )

    def create(self, request, *args, **kwargs):
        # Wszyscy zalogowani mogą tworzyć grupy
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Jeśli to student, nie może ustawiać prowadzącego ani tematu
        if not (request.user.groups.filter(name='lecturer').exists() or request.user.is_staff):
            if 'lecturer' in request.data:
                self.permission_denied(
                    request,
                    message='Student nie może przypisywać prowadzącego do grupy.'
                )
            if 'topic' in request.data:
                self.permission_denied(
                    request,
                    message='Student nie może przypisywać tematu do grupy.'
                )
        
        self.perform_create(serializer)
        
        # Jeśli to student, automatycznie dodaj go do stworzonej grupy
        if not (request.user.groups.filter(name='lecturer').exists() or request.user.is_staff):
            created_group = Group.objects.get(id=serializer.data['id'])
            request.user.student_group = created_group
            request.user.save()
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @list_route(methods=['get'], url_path='get-group')
    def get_user_group(self, request):
        """Pobierz grupę aktualnego użytkownika"""
        if not request.user.student_group:
            return Response({'detail': 'Nie jesteś w żadnej grupie.'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        instance = Group.objects.filter(id=request.user.student_group.id).first()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @list_route(methods=['get'], url_path='all-with-preferences')
    def get_all_with_preferences(self, request):
        """
        Zwraca wszystkie grupy z informacjami dla prowadzącego
        TYLKO DLA PROWADZĄCYCH!
        """
        # Sprawdź czy użytkownik jest wykładowcą
        if not (request.user.groups.filter(name='lecturer').exists() or request.user.is_staff):
            return Response(
                {'detail': 'Tylko wykładowcy mogą przeglądać wszystkie grupy.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        from users.models import AppUser
        from preferences.models import Preference
        
        groups = Group.objects.all()
        
        data = []
        for group in groups:
            # Policz studentów w grupie
            student_count = AppUser.objects.filter(student_group=group).count()
            
            # Pobierz preferencje tej grupy
            preferences = Preference.objects.filter(group=group).order_by('priority')
            preferences_data = []
            for pref in preferences:
                preferences_data.append({
                    'priority': pref.priority,
                    'topic_id': pref.topic.id,
                    'topic_name': pref.topic.name_topic,
                    'topic_description': pref.topic.descriprion
                })
            
            group_data = {
                'id': group.id,
                'name': group.name_group,
                'code': group.code,
                'lecturer': group.lecturer.username if group.lecturer else None,
                'lecturer_id': group.lecturer.id if group.lecturer else None,
                'assigned_topic': {
                    'id': group.topic.id,
                    'name': group.topic.name_topic,
                    'description': group.topic.descriprion
                } if group.topic else None,
                'student_count': student_count,
                'students': list(group.appuser_set.values('id', 'username', 'first_name', 'last_name')),
                'preferences': preferences_data
            }
            data.append(group_data)
        
        return Response(data, status=status.HTTP_200_OK)
    
    @detail_route(methods=['post'], url_path='join')
    def join_group(self, request, pk=None):
        """Dołącz do grupy przez kod"""
        group = self.get_object()
        code = request.data.get('code')
        
        if not code:
            return Response(
                {'detail': 'Podaj kod grupy.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if group.code != code:
            return Response(
                {'detail': 'Nieprawidłowy kod grupy.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Sprawdź czy użytkownik już ma grupę
        if request.user.student_group:
            return Response(
                {'detail': 'Już należysz do grupy. Najpierw opuść obecną.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Dołącz do grupy
        request.user.student_group = group
        request.user.save()
        
        return Response(
            {'detail': f'Dołączyłeś do grupy: {group.name_group}'},
            status=status.HTTP_200_OK
        )
    
    @list_route(methods=['post'], url_path='leave')
    def leave_group(self, request):
        """Opuść obecną grupę"""
        if not request.user.student_group:
            return Response(
                {'detail': 'Nie jesteś w żadnej grupie.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_group = request.user.student_group
        request.user.student_group = None
        request.user.save()
        
        return Response(
            {'detail': f'Opuściłeś grupę: {old_group.name_group}'},
            status=status.HTTP_200_OK
        )
