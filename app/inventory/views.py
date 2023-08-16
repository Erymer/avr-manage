'''
Views for the inventory API.
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import EquipmentType, EquipmentModel, EquipmentBrand, Equipment
from inventory.permissions import InventoryPermissions

from inventory import serializers

class EquipmentTypeViewSet(viewsets.ModelViewSet):
    """View for manage equipment type APIs"""
    serializer_class = serializers.EquipmentTypeSerializer
    queryset = EquipmentType.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        InventoryPermissions,
    ]


class EquipmentModelViewSet(viewsets.ModelViewSet):
    """View for manage equipment model APIs"""
    serializer_class = serializers.EquipmentModelSerializer
    queryset = EquipmentModel.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        InventoryPermissions,
    ]


class EquipmentBrandViewSet(viewsets.ModelViewSet):
    """View for manage equipment brand APIs"""
    serializer_class = serializers.EquipmentBrandSerializer
    queryset = EquipmentBrand.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        InventoryPermissions,
    ]


class EquipmentViewSet(viewsets.ModelViewSet):
    """View for manage equipment APIs"""
    serializer_class = serializers.EquipmentSerializer
    queryset = Equipment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        InventoryPermissions,
    ]

