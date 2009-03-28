from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^find-weather-locations/$', 'weathertracking.views.find_weather_stations'),
)
