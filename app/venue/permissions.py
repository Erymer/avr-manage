'''
Permissions for Venue API
'''

from rest_framework.permissions import BasePermission

# Available employee roles
# - 'sales'
# - 'tech'
# - 'admin'
# - 'finance'

class VenueCreatePermissions(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = ['sales']
        return request.user.is_authenticated and request.user.role in allowed_roles

class VenueReadPermissions(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

class VenueUpdatePermissions(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = ['sales']
        return request.user.is_authenticated and request.user.role in allowed_roles

class VenueDeletePermissions(BasePermission):
    def has_permission(self, request, view):
        allowed_roles = ['sales']
        return request.user.is_authenticated and request.user.role in allowed_roles

