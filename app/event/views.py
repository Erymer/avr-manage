from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from event import serializers

from core.models import Event, EventPhoto
from event.permissions import EventPermissions


class EventViewSet(viewsets.ModelViewSet):
    """View for manage event API"""
    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        EventPermissions,
    ]

class EventPhotoViewSet(viewsets.ModelViewSet):
    """View for manage event API"""
    serializer_class = serializers.EventPhotoSerializer
    queryset = EventPhoto.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        EventPermissions,
    ]

