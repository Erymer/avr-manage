from rest_framework import serializers
from core.models import (
    Customer,
    Equipment,
    Event, 
    Venue,
)
from django.contrib.auth import get_user_model

class VenueSerializer(serializers.ModelSerializer):
    '''Venue model serializer for Event model'''
    class Meta:
        model = Venue
        fields = ['id']


class EquipmentSerializer(serializers.ModelSerializer):
    '''Equipment model serializer for Event model'''
    class Meta:
        model = Equipment
        fields = ['uid']


class CustomerSerializer(serializers.ModelSerializer):
    '''Customer model serializer for Event model'''
    class Meta:
        model = Customer
        fields = ['id']


class CrewSerializer(serializers.ModelSerializer):
    '''Crew model serializer for Event model'''
    class Meta:
        model = get_user_model()
        fields = ['username']


class EventSerializer(serializers.ModelSerializer):
    '''Serializer for Event model'''
    venue = VenueSerializer
    equipment = EquipmentSerializer
    customer = CustomerSerializer
    crew = CrewSerializer
    leader = CrewSerializer

    class Meta: 
        model = Event
        fields = '__all__'
        read_only_fields = ['id']
