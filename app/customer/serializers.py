"""
Serializers for customer APIs
"""

from rest_framework import serializers
from core.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for client instances."""

    class Meta:
        model = Customer
        fields = '__all__'
        read_only_fields = ['id']
