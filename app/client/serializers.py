"""
Serializers for client APIs
"""

from rest_framework import serializers
from core.models import Client

class ClientSerializer(serializers.ModelSerializer):
    """Serializer for client instances."""

    class Meta:
        model = Client
        fields = ['id', 'name', 'phone', 'email']
        read_only_fields = ['id']
