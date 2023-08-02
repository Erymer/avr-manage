'''
Views for the venues API.
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Venue
from venue.permissions import VenuePermissions

from venue import serializers

class VenueViewSet(viewsets.ModelViewSet):
    """View for manage venue APIs"""
    serializer_class = serializers.VenueSerializer
    queryset = Venue.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        VenuePermissions
    ]

    
    # def get_permissions(self):
    #     '''
    #     Define venue permissions
    #     '''

    #     if self.action in ['list', 'retrieve']:
    #         return [VenueReadPermissions()]

    #     elif self.action in ['create']:
    #         return [VenueCreatePermissions()]

    #     elif self.action in ['update']:
    #         return [VenueUpdatePermissions()]

    #     elif self.action in ['partial_update']:
    #         return [VenueUpdatePermissions()]

    #     elif self.action in ['destroy']:
    #         return [VenueDeletePermissions()]

    #     return super().get_permissions()
