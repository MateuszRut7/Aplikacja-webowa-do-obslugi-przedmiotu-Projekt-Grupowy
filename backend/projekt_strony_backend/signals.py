from django.conf import settings
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Permissions(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        user = request.user
        
        if not user.is_authenticated:
            return Response([])
        
        # Pobierz nazwy grup użytkownika
        groups = list(user.groups.values_list('name', flat=True))
        
        # Jeśli użytkownik jest staff (is_staff=True) i nie ma grupy 'lecturer', dodaj ją
        if user.is_staff and 'lecturer' not in groups:
            # Dodaj użytkownika do grupy 'lecturer' jeśli istnieje
            from django.contrib.auth.models import Group
            lecturer_group, created = Group.objects.get_or_create(name='lecturer')
            user.groups.add(lecturer_group)
            groups.append('lecturer')
        
        # Jeśli użytkownik nie ma żadnej grupy, domyślnie 'student'
        if not groups:
            groups = ['student']
        
        return Response(groups)
