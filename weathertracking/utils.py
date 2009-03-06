from django.contrib.gis.db.backend import SpatialBackend
from weathertracking.models import WeatherStation

def find_nearest_weather_stations(pt, qty=5):
    """Expects a django.contrib.gis.geos.Point for the location to look for
    the nearest weather stations to. Returns a queryset of _qty_ (default 5)
    weathertracking.models.WeatherStation instances sorted in order of
    ascending distance. Also available is a 'distance' and 'azimuth' property."""

    return WeatherStation.objects.all().distance(pt).order_by('distance').extra(select={'azimuth': 'ST_Azimuth(%s, point)'}, select_params=(SpatialBackend.Adaptor(pt),))[:qty]

def find_nearest_weather_station(pt):
    """Expects a django.contrib.gis.geos.Point for the location to look for
    the nearest weather station to. Returns a weathertracking.models.WeatherStation
    instance. Also available is a 'distance' and 'azimuth' property."""

    return WeatherStation.objects.all().distance(pt).order_by('distance').extra(select={'azimuth': 'ST_Azimuth(%s, point)'}, select_params=(SpatialBackend.Adaptor(pt),))[:1][0]
