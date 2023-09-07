'''
Views for the customers API.
'''

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Customer
from customer.permissions import CustomerPermissions

from customer import serializers

class CustomerViewSet(viewsets.ModelViewSet):
    """View for manage client APIs"""
    serializer_class = serializers.CustomerSerializer
    queryset = Customer.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        IsAuthenticated,
        CustomerPermissions
    ]
