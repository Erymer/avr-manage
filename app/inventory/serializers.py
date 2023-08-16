"""
Serializers for inventory APIs
"""

from rest_framework import serializers
from core.models import (
    EquipmentType, 
    EquipmentBrand, 
    EquipmentModel,
    Equipment
)
from rest_framework.exceptions import ValidationError

class EquipmentTypeSerializer(serializers.ModelSerializer):
    """Serializer for Equipment Type."""

    class Meta:
        model = EquipmentType
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        name = validated_data.get('name')
        instance, created = EquipmentType.objects.get_or_create(name=name)       
        return instance


class EquipmentBrandSerializer(serializers.ModelSerializer):
    """Serializer for Equipment Brand."""

    class Meta:
        model = EquipmentBrand
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        name = validated_data.get('name')
        instance, created = EquipmentBrand.objects.get_or_create(name=name)       
        return instance


class EquipmentModelSerializer(serializers.ModelSerializer):
    """Serializer for Equipment Model."""

    class Meta:
        model = EquipmentModel
        fields = '__all__'
        read_only_fields = ['id']

    def create(self, validated_data):
        name = validated_data.get('name')
        instance, created = EquipmentModel.objects.get_or_create(name=name)       
        return instance


class EquipmentDataSerializer(serializers.Serializer):
    """Serializer for Equipment Model."""
    name = serializers.CharField(max_length=50)


class EquipmentSerializer(serializers.ModelSerializer):

    model = EquipmentDataSerializer()
    brand = EquipmentDataSerializer()
    type = EquipmentDataSerializer()

    class Meta:
        model = Equipment
        fields = '__all__'
        read_only_fields = ['id', 'uid']


    def create(self, validated_data):
        model_data = validated_data.pop('model')
        brand_data = validated_data.pop('brand')
        type_data = validated_data.pop('type')
        equipment_model, _ = EquipmentModel.objects.get_or_create(**model_data)
        equipment_brand, _ = EquipmentBrand.objects.get_or_create(**brand_data)
        equipment_type, _ = EquipmentType.objects.get_or_create(**type_data)
        equipment = Equipment.objects.create(
            model=equipment_model,
            brand=equipment_brand,
            type=equipment_type,
            **validated_data
        )
        return equipment


    def update(self, instance, validated_data):
        if 'model' in validated_data:
            model_data = validated_data.pop('model')
            equipment_model, _ = EquipmentModel.objects.get_or_create(**model_data)
            instance.model = equipment_model

        if 'brand' in validated_data:
            brand_data = validated_data.pop('brand')
            equipment_brand, _ = EquipmentBrand.objects.get_or_create(**brand_data)
            instance.brand = equipment_brand

        if 'type' in validated_data:
            type_data = validated_data.pop('type')
            equipment_type, _ = EquipmentType.objects.get_or_create(**type_data)
            instance.type = equipment_type

        instance.number = validated_data.get('number', instance.number)
        instance.serial_number = validated_data.get('serial_number', instance.serial_number)
        instance.save()

        return instance
