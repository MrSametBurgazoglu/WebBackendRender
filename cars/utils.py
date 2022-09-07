from django.db.models.expressions import RawSQL
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from accounts.models import Customer
from cars.models import Car, Location


def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    gcd_formula = "6371 * acos(least(greatest(\
    cos(radians(%s)) * cos(radians(latitude)) \
    * cos(radians(longitude) - radians(%s)) + \
    sin(radians(%s)) * sin(radians(latitude)) \
    , -1), 1))"
    distance_raw_sql = RawSQL(
        gcd_formula,
        (latitude, longitude, latitude)
    )
    qs = Car.objects.all().select_related('location').annotate(distance=distance_raw_sql).order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs


def create_token(user):
    token = Token.objects.create(user=user)
    return token


def create_customer():
    user = User.objects.create(
        username="MrSametBurgazoğlu",
        email="sametburgazoglu@gmail.com",
    )
    user.set_password("54M3754m37")
    user.save()
    customer = Customer.objects.create(
        phone="123213123",
        name=user.username,
        email=user.email,
        user=user,
    )
    customer.save()
    return customer


def create_test_cars():
    location1 = Location.objects.create(latitude=1.0, longitude=1.0)
    location2 = Location.objects.create(latitude=111.0, longitude=1.0)
    location3 = Location.objects.create(latitude=1.0, longitude=111.0)
    location4 = Location.objects.create(latitude=1.0, longitude=1.0)
    location5 = Location.objects.create(latitude=1.0, longitude=1.0)
    location1.save()
    location2.save()
    location3.save()
    location4.save()
    location5.save()
    Car.objects.bulk_create([
        Car(brand="brand", model="model", segment="segment", licence="ABC 123 ABC", location=location1),
        Car(brand="brand", model="model", segment="segment", licence="ABC 124 ABC", location=location2),
        Car(brand="brand", model="model", segment="segment", licence="ABC 125 ABC", location=location3),
        Car(brand="brand", model="model", segment="segment", licence="ABC 126 ABC", location=location4),
        Car(brand="brand", model="model", segment="segment", licence="ABC 127 ABC", location=location5),
    ])
