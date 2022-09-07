from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core import exceptions
from django.shortcuts import get_object_or_404

from rest_framework import serializers

from accounts.models import Customer, PaymentMethod, Address
from cars.serializers import LocationSerializer


class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = ('information', 'name', 'owner_name', 'number', 'csv', 'last_month', 'last_year')


class AdressSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Address


class CustomerSerializer(serializers.ModelSerializer):
    address = AdressSerializer(read_only=True)
    # payment_method = PaymentMethodSerializer()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Customer
        fields = ['name', 'phone', 'email', 'driver_licence', 'address', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        customer = Customer.objects.create(
            phone=validated_data['phone'],
            name=user.username,
            email=user.email,
            user=user,
        )
        customer.save()
        return customer

    def update(self, instance, validated_data):
        user = instance.user
        if 'name' in validated_data:
            instance.name = validated_data['name']
            user.username = validated_data['name']
        if 'email' in validated_data:
            instance.email = validated_data['email']
            user.email = validated_data['email']
        if 'phone' in validated_data:
            instance.phone = validated_data['phone']
        user.save()
        instance.save()
        return instance


class AuthCustomTokenSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            validate_email(email)
            user_request = get_object_or_404(
                User,
                email=email,
            )
            user = authenticate(username=user_request.username, password=password)
            attrs['user'] = user
            if user:
                if not user.is_active:
                    raise exceptions.ValidationError('User account is disabled.')
            else:
                raise exceptions.ValidationError('Unable to log in with provided credentials.')
        else:
            raise exceptions.ValidationError('Must include "email" and "password"')
        return attrs
