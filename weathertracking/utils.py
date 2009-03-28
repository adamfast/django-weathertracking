import urllib
from django.contrib.gis.db.backend import SpatialBackend
from django.contrib.gis.geos import Point
from weathertracking.models import WeatherStation

def find_nearest_weather_stations_to_location(location, qty=5):
    location = urllib.quote_plus(location)
    request = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, "csv", settings.GOOGLE_MAPS_KEY)
    data = urllib.urlopen(request).read()
    dlist = data.split(',')
    if dlist[0] == '200':
        point = Point((float(dlist[3]), float(dlist[2])),)

    return find_nearest_weather_stations(point, qty)

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
