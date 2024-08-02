from rest_framework import permissions
from guardian.shortcuts import get_perms


class CategoryPermission(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == 'create':
            return user.has_perm('catalog.add_category')
        elif view.action in ['update', 'partial_update']:
            return user.has_perm('catalog.change_category')
        elif view.action == 'destroy':
            return user.has_perm('catalog.delete_category')

        return False


class ColorPermission(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == 'create':
            return user.has_perm('catalog.add_color')
        elif view.action in ['update', 'partial_update']:
            return user.has_perm('catalog.change_color')
        elif view.action == 'destroy':
            return user.has_perm('catalog.delete_color')

        return False


class SizePermission(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == 'create':
            return user.has_perm('catalog.add_size')
        elif view.action in ['update', 'partial_update']:
            return user.has_perm('catalog.change_size')
        elif view.action == 'destroy':
            return user.has_perm('catalog.delete_size')

        return False


class ProductPermission(permissions.BasePermission):
    """
    Custom permission to only allow users to edit their own data.
    """

    def has_permission(self, request, view):

        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if not user.is_authenticated:
            return False

        if view.action == 'create':
            return user.has_perm('catalog.add_product')
        elif view.action in ['update', 'partial_update']:
            return user.has_perm('catalog.change_product')
        elif view.action == 'destroy':
            return user.has_perm('catalog.delete_product')

        return False
