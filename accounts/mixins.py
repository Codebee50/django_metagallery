from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

class IsAdminMixin():
    permission_classes = [IsAuthenticated, IsAdmin]