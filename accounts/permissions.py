
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permits only admins from using put, patch, post, delete methods.
    
    ---
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_admin



class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_admin