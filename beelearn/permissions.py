from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.permissions import BasePermission


class IsAdminOnlyAction(BasePermission):
    def has_permission(self, request: Request, view: APIView):
        if request.method in view.ADMIN_ONLY_ACTIONS:
            return bool(request.user and request.user.is_staff)

        return bool(request.user and request.user.is_authenticated)
