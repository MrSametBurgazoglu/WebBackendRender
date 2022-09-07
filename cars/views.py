from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from cars.serializers import CarSerializer, CarDetailSerializer
from cars.models import Car
from cars.utils import get_locations_nearby_coords


class CarsViewSet(viewsets.ViewSet, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):  # TODO-ERROR FIX THIS
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CarSerializer
    queryset = Car.objects.all()

    def get_permissions(self):
        if self.action in ["create", "update", "destroy", "partial update", "change state"]:
            self.permission_classes = [IsAuthenticated]
        else:#create
            self.permission_classes = [AllowAny]
        return super(CarsViewSet, self).get_permissions()

    def list(self, request):
        print(request.GET)
        print(request.json())
        print(request.body())
        longitude = request.GET.get('longitude')
        latitude = request.GET.get('latitude')
        radius = 10.0
        try:
            longitude = float(longitude)
            latitude = float(latitude)
            locations = get_locations_nearby_coords(latitude, longitude, radius)
            serializer = CarSerializer(locations, many=True)
            return Response(serializer.data)
        except TypeError:
            return JsonResponse({"error": "longitude and latitude must be numbers", "longitude": longitude, "latitude": latitude})

    # TODO ADD TRY-EXCEPT
    def retrieve(self, request, pk=None):
        car = get_object_or_404(Car, pk=pk)
        serializer = CarDetailSerializer(car)
        return Response(serializer.data)

    # TODO ADD TRY-EXCEPT
    @action(detail=True, methods=['post'])
    def change_state(self, request, pk=None):
        """
        change state of the car
        """
        car = get_object_or_404(Car, pk=pk)
        car.active = not car.active
        car.save()
        return Response({"success": "True"})