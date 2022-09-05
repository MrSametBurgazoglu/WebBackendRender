from django.contrib.auth.models import User, Group
from accounts.models import Customer, PaymentMethod
from cars.serializers import LocationSerializer
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.shortcuts import get_object_or_404


class UsersSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
'''
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2',
                  'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return JsonResponse({'user_id': user.id})

'''
class PaymentMethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = PaymentMethod
        fields = ('information', 'name', 'owner_name', 'number', 'csv', 'last_month', 'last_year')

class CustomerSerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)
    #payment_method = PaymentMethodSerializer()
    user = UsersSerializer()

    class Meta:
        model = Customer
        fields = ['phone_number', 'location', 'user', 'full_address']

    def create(self, validated_data):
        user_data = validated_data['user']
        user = User.objects.create(
            username=user_data['username'],
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )
        user.set_password(user_data['password'])
        user.save()
        customer = Customer.objects.create(
            phone_number=validated_data['phone_number'],
            full_name=" ".join([user.first_name, user.last_name]),
            email=user.email,
            user=user,
        )
        customer.save()
        return customer

    def update(self, instance, validated_data):
        user = instance.user
        if 'user' in validated_data:
            user_data = validated_data['user']
            fields = ['username', 'email', 'first_name', 'last_name']
            for attr in fields:
                if attr in user_data:
                    setattr(user, attr, user_data[attr])
        customer_fields = ['phone_number', 'full_name']
        for attr in customer_fields:
            if attr in validated_data:
                setattr(instance, attr, validated_data[attr])
        instance.email = user.email
        instance.full_name = " ".join([user.first_name, user.last_name])
        user.save()
        instance.save()
        return instance
