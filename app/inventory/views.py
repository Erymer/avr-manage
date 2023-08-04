'''
Views for the inventory API.
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import EquipmentType
from inventory.permissions import EquipmentTypePermissions

from inventory import serializers

class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """View for manage venue APIs"""
    serializer_class = serializers.EquipmentTypeSerializer
    queryset = EquipmentType.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        EquipmentTypePermissions,
    ]
