from rest_framework import permissions

class IsLecturer(permissions.BasePermission):
    """
    Pozwala dostęp tylko wykładowcom (użytkownicy z grupą 'lecturer' lub is_staff=True)
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.groups.filter(name='lecturer').exists() or 
            request.user.is_staff
        )

class IsStudent(permissions.BasePermission):
    """
    Pozwala dostęp tylko studentom (użytkownicy z grupą 'student')
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
               request.user.groups.filter(name='student').exists()

class IsGroupMemberOrLecturer(permissions.BasePermission):
    """
    Pozwala dostęp członkom grupy lub wykładowcom
    """
    def has_object_permission(self, request, view, obj):
        # Wykładowcy mają pełny dostęp
        if request.user.groups.filter(name='lecturer').exists() or request.user.is_staff:
            return True
        
        # Studenci: sprawdź czy użytkownik należy do tej grupy
        if hasattr(obj, 'appuser_set'):  # Dla modelu Group
            return obj.appuser_set.filter(id=request.user.id).exists()
        elif hasattr(obj, 'student_group'):  # Dla modelu AppUser
            return obj.student_group == request.user.student_group
        elif hasattr(obj, 'group'):  # Dla modelu Preference
            return obj.group == request.user.student_group
        
        return False
