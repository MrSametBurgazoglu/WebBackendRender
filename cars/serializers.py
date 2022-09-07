from rest_framework import serializers
from cars.models import Car, Location, Pricing


class PricingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pricing
        fields = ['minute', 'hourly', 'daily', 'extra_kilometer']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['location_text', 'longitude', 'latitude']


class CarSerializer(serializers.ModelSerializer):
    #location = LocationSerializer(read_only=True)
    #pricing = PricingSerializer(read_only=True)

    class Meta:
        model = Car
        fields = ['brand', 'model', 'segment', 'licence', 'year',
                  'fuel_type', 'passenger_capacity', 'gear_type']

    def create(self, validated_data):
        return Car.objects.create(**validated_data)

    def update(self, instance, validated_data):  # TODO update only necessary variables
        instance.brand = validated_data.get('brand', instance.brand)
        instance.model = validated_data.get('model', instance.model)
        instance.segment = validated_data.get('segment', instance.segment)
        instance.licence = validated_data.get('licence', instance.licence)
        instance.save()
        return instance


class CarDetailSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Car
        fields = ['brand', 'model', 'segment', 'licence', 'year', 'fuel_type', 'passenger_capacity', 'gear_type']
