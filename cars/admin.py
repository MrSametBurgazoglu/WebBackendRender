from django.contrib import admin
from cars.models import Car, Location


class CarAdmin(admin.ModelAdmin):

    list_display = ['brand', 'model', 'licence']

    class Meta:
        model = Car


class LocationAdmin(admin.ModelAdmin):

    list_display = ['location_text']

    class Meta:
        model = Location


admin.site.register(Car, CarAdmin)
admin.site.register(Location, LocationAdmin)
