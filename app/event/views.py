from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from event import serializers

from core.models import Event
from event.permissions import EventPermissions

# from event import serializers

class EventViewSet(viewsets.ModelViewSet):
    """View for manage event API"""
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        EventPermissions,
    ]

