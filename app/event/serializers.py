from rest_framework import serializers
from core.models import (
    Event, 
    Venue,
    Customer,
    Equipment,
    EventPhoto,
)
from django.contrib.auth import get_user_model

class VenueSerializer(serializers.Serializer):
    '''Venue model serializer for Event model'''
    id = serializers.IntegerField()


class EquipmentSerializer(serializers.Serializer):
    '''Equipment model serializer for Event model'''
    uid = serializers.CharField(max_length=50)


class EquipmentListSerializer(serializers.ListSerializer):
    '''Crew model serializer for Event model'''
    child = EquipmentSerializer()


class CustomerSerializer(serializers.Serializer):
    '''Customer model serializer for Event model'''
    id = serializers.IntegerField()


class CrewMemberSerializer(serializers.Serializer):
    '''Crew model serializer for Event model'''
    username = serializers.CharField(max_length=50)


class CrewSerializer(serializers.ListSerializer):
    '''Crew model serializer for Event model'''
    child = CrewMemberSerializer()


class EventSerializer(serializers.ModelSerializer):
    '''Serializer for Event model'''
    venue = VenueSerializer()
    equipment = EquipmentListSerializer()
    customer = CustomerSerializer()
    crew = CrewSerializer()
    leader = CrewMemberSerializer()

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        leader_data = validated_data.pop('leader')
        venue_data = validated_data.pop('venue')
        customer_data = validated_data.pop('customer')
        equipment_data = validated_data.pop('equipment')
        crew_data = validated_data.pop('crew')

        equipment_list = [Equipment.objects.get(**e) for e in equipment_data]
        crew_list = [get_user_model().objects.get(**c) for c in crew_data]

        leader = get_user_model().objects.get(**leader_data)
        venue = Venue.objects.get(**venue_data)
        customer = Customer.objects.get(**customer_data)

        event = Event.objects.create(
            venue=venue,
            leader=leader,
            customer=customer,
            **validated_data
        )
        event.equipment.set(equipment_list)
        event.crew.set(crew_list)
        return event


    # TODO: Create exceptions in case of trying to get an instance that doesnt exists. It should return an error.
    def update(self, instance, validated_data):
        if 'venue' in validated_data:
            venue_data = validated_data.pop('venue')
            venue = Venue.objects.get(**venue_data)
            instance.venue = venue

        if 'leader' in validated_data:
            leader_data = validated_data.pop('leader')
            leader = get_user_model().objects.get(**leader_data)
            instance.leader = leader

        if 'customer' in validated_data:
            customer_data = validated_data.pop('customer')
            customer = Customer.objects.get(**customer_data)
            instance.customer = customer

        if 'crew' in validated_data:
            crew_data = validated_data.pop('crew')
            crew_list = [get_user_model().objects.get(**c) for c in crew_data]
            instance.crew.set(crew_list)

        if 'equipment' in validated_data:
            equipment_data = validated_data.pop('equipment')
            equipment_list = [Equipment.objects.get(**e) for e in equipment_data]
            instance.equipment.set(equipment_list)

        instance.name = validated_data.get('name', instance.name)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.load_in_date = validated_data.get('load_in_date', instance.load_in_date)
        instance.load_out_date = validated_data.get('load_out_date', instance.load_out_date)
        instance.start_date = validated_data.get('start_date', instance.start_date)
        instance.end_date = validated_data.get('end_date', instance.end_date)
        instance.save()

        return instance


# TODO: There must be a better way to do this
class EventDataSerializer(serializers.Serializer):
    '''Customer model serializer for Event model'''
    id = serializers.IntegerField()

class EventPhotoSerializer(serializers.ModelSerializer):
    '''Serializer for Event model'''
    event = EventDataSerializer()

    class Meta:
        model = EventPhoto
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        event_data = validated_data.pop('event')
        event = Event.objects.get(**event_data)

        event_photo = EventPhoto.objects.create(
            event=event,
            **validated_data
        )
        return event_photo

