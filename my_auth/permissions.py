from rest_framework import permissions
from django.contrib.auth import get_user_model
User = get_user_model()


class UserPermission(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            if view.action == 'signup':
                return True

            return False

        if view.action in ['update', 'partial_update']:
            return True

        return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'list':
            return True
        if view.action == 'retrieve':
            return True

        user = request.user
        if not user.is_authenticated:
            if view.action == 'signup':
                return True
            return False

        if view.action in ['update', 'partial_update']:
            return user.has_perm('my_auth.change_user', obj)
        elif view.action == 'destroy':
            return user.has_perm('my_auth.delete_user', obj)

        return False


class IsAnonymousUser(permissions.BasePermission):
    """
    Custom permission to check if user is not authenticated.
    """

    def has_permission(self, request, view):
        return not request.user.is_authenticated
