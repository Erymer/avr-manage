"""
Serializers for inventory APIs
"""

from rest_framework import serializers
from core.models import EquipmentType

class EquipmentTypeSerializer(serializers.ModelSerializer):
    """Serializer for Equipment."""

    class Meta:
        model = EquipmentType
        fields = ['id', 'name']
        read_only_fields = ['id']
