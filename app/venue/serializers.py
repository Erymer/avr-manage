"""
Serializers for venue APIs
"""

from rest_framework import serializers
from core.models import Venue

class VenueSerializer(serializers.ModelSerializer):
    """Serializer for venues."""

    class Meta:
        model = Venue
        fields = ['id', 'name', 'address', 'city', 'state']
        read_only_fields = ['id']
