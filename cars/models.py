from django.db import models

class Pricing(models.Model):
    minute = models.FloatField(default=0)
    hourly = models.FloatField(default=0)
    daily = models.FloatField(default=0)
    extra_kilometer = models.FloatField(default=0)


class Location(models. Model):
    location_text = models.CharField(verbose_name="Full Location", max_length=256)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


# get : brand, model, segment, year, fuel_type, price_minute, price_hour, passenger_capacity, gear_type, locations
class Car(models.Model):
    photo = models.ImageField(verbose_name="A photo of car", upload_to=None, height_field=None, width_field=None, null=True)
    brand = models.CharField(verbose_name="Brand", max_length=32)
    model = models.CharField(verbose_name="Model", max_length=128)
    segment = models.CharField(verbose_name="Segment", max_length=128)
    year = models.DateTimeField(verbose_name="The year car build", null=True)
    join_year = models.DateTimeField(verbose_name="When the car is added to the system", auto_now_add=True)
    current_fuel_quantity = models.IntegerField(verbose_name="Current fuel quantity", default=0)
    total_km = models.IntegerField(default=0)
    total_fuel_quantity = models.IntegerField(verbose_name="Total fuel quantity", default=0)
    body = models.CharField(default="", max_length=16)
    price = models.ForeignKey(Pricing, on_delete=models.CASCADE, null=True)
    fuel_type = models.CharField(verbose_name="Fuel type", default="Gasoline", max_length=64)
    active = models.BooleanField(verbose_name="Active", default=False)
    passenger_capacity = models.IntegerField(verbose_name="Passenger Capacity", default=1)
    gear_type = models.CharField(max_length=32)
    licence = models.CharField(verbose_name="Licence", max_length=32, default="")
    location = models.OneToOneField(Location, on_delete=models.CASCADE, null=True, blank=True)
    # TODO ADD QR_CODE

    class Meta:
        ordering = ['join_year']

    def __str__(self):
        return self.licence

# Create your models here.
