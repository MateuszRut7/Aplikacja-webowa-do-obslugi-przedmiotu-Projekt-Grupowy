from .models import AppUser
from .serializers import AppUserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import list_route, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from groups.models import Group


class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
    filter_fields = '__all__'
    filter_backends = (OrderingFilter, DjangoFilterBackend)
    ordering_fields = '__all__'

    @list_route(methods=('PATCH',), url_path='add-group')
    def add_to_group(self, request, *args, **kwargs):
        # POPRAWKA: Pobierz kod z JSON lub z form-data
        if isinstance(self.request.data, dict):
            code = self.request.data.get('code', '')
        else:
            code = str(self.request.data)
        
        group = Group.objects.filter(code=code)
        if not group.exists():
            return Response({
                'detail': ('Taka grupa nie istnieje')
            }, status=status.HTTP_400_BAD_REQUEST)
        user = self.request.user
        user.student_group = group.first()
        user.save()
        return Response(status=status.HTTP_201_CREATED)

    @list_route(methods=('GET',), url_path='get-group')
    def get_group(self, request, *args, **kwargs):
        data = True
        if self.request.user.student_group is None:
            data = False
        return Response(data, status=status.HTTP_200_OK)

    @list_route(methods=('GET',), url_path='leave-group')
    def leave_group(self, request, *args, **kwargs):
        user = self.request.user
        user.student_group = None
        user.save()
        return Response(status=status.HTTP_200_OK)

    def list(self, request):
        user = self.request.user
        
        # POPRAWKA: Jeśli user nie ma student_group (np. wykładowca), zwróć pusty queryset
        if user.student_group is None:
            queryset = AppUser.objects.none()
        else:
            queryset = AppUser.objects.filter(student_group=user.student_group)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# DODAJ TE FUNKCJĘ POZA KLASĄ - jako oddzielną funkcję
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Zwraca dane aktualnie zalogowanego użytkownika"""
    serializer = AppUserSerializer(request.user)
    return Response(serializer.data)


# DODAJ NOWY ENDPOINT DLA WYKŁADOWCÓW
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def lecturers_list(request):
    """Zwraca listę wykładowców (is_staff=True)"""
    # Tylko zalogowani użytkownicy
    lecturers = AppUser.objects.filter(is_staff=True)
    serializer = AppUserSerializer(lecturers, many=True)
    return Response(serializer.data)
