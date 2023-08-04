'''
Views for the clients API.
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Client
from client.permissions import ClientPermissions

from client import serializers

class ClientViewSet(viewsets.ModelViewSet):
    """View for manage client APIs"""
    serializer_class = serializers.ClientSerializer
    queryset = Client.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        ClientPermissions
    ]
