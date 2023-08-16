'''
Permissions for Inventory API
'''

from rest_framework.permissions import BasePermission

# Available employee roles
# - 'sales'
# - 'tech'
# - 'admin'
# - 'finance'
# - 'inventory'

class InventoryPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:
            return request.user.is_authenticated

        elif request.method in ['POST']:
            allowed_roles = ['inventory']
            return request.user.is_authenticated and request.user.role in allowed_roles

        elif request.method in ['PUT']:
            allowed_roles = ['inventory']
            return request.user.is_authenticated and request.user.role in allowed_roles

        elif request.method in ['PATCH']:
            allowed_roles = ['inventory']
            return request.user.is_authenticated and request.user.role in allowed_roles

        elif request.method in ['DELETE']:
            allowed_roles = ['inventory']
            return request.user.is_authenticated and request.user.role in allowed_roles
