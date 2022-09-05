from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, generics
from rest_framework import permissions
from accounts.serializers import CustomerSerializer
from accounts.models import Customer
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

class UserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, pk=None):
        user = get_object_or_404(User, pk=pk)
        serializer = CustomerSerializer(user.customer)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def change_state(self, request, pk=None):
        """
        change state of the user
        """
        user = get_object_or_404(User, pk=pk)
        user.active = not user.active
        user.save()
        return Response({"success": "True"})


'''
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
'''


class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy", "list", "retrieve"]:
            return (IsAuthenticated(),)
        else:
            return (AllowAny(),)
