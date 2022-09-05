from django.db.models.expressions import RawSQL
from cars.models import Location, Car


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