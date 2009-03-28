import urllib
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.maps.google import GoogleMap
from django.contrib.gis.maps.google.overlays import GMarker, GEvent
from django.shortcuts import get_object_or_404, render_to_response
from django.template.defaultfilters import floatformat
from weathertracking.templatetags.weathertracking import m_to_ft, rad_to_deg
from weathertracking.utils import find_nearest_weather_stations

def find_weather_stations(request):
    if request.method == 'POST':
        location = urllib.quote_plus(request.POST['location'])
        request_url = "http://maps.google.com/maps/geo?q=%s&output=%s&key=%s" % (location, "csv", settings.GOOGLE_MAPS_API_KEY)
        data = urllib.urlopen(request_url).read()
        dlist = data.split(',')
        if dlist[0] == '200':
            point = Point((float(dlist[3]), float(dlist[2])),)

        markers = []

        marker = GMarker(point, request.POST['location'])
        marker.add_event(GEvent('click', 'function() { geodjango.map_marker1.openInfoWindowHtml("%s") }' % request.POST['location']))
#        # the gis.maps.google.* stuff doesn't allow for ^^^^^ dynamic naming of these - with multiple points, it will be
#        # necessary to for loop through the points with your own counter (start from zero) and that should coincide with
#        # the template forloop counter being used - but by all means cross-check that every time to make sure it's right.
        markers.append(marker)

        weather_stations = find_nearest_weather_stations(point, qty=10)

        count = 2
        for station in weather_stations:
            marker = GMarker(station.point, '%s %s' % (station.code, station.get_name()))
            marker.add_event(GEvent('click', 'function() { geodjango.map_marker%s.openInfoWindowHtml("%s"); }' % \
                (count, "%s, (altitude %s ft.) - %s mi @ %s deg""" \
                % (station.code, floatformat(m_to_ft(station.elevation), 0), floatformat(station.distance.mi, 2), floatformat(rad_to_deg(station.azimuth))))
            ))
            markers.append(marker)
            count = count + 1

        map = GoogleMap(key=settings.GOOGLE_MAPS_API_KEY, markers=markers)

        return render_to_response('locationfinder.html', {
            'location': request.POST['location'],
            'location_point': point,
            'google': map,
            'weather_stations': weather_stations,
        })
    else:
        return render_to_response('locationfinder.html', {})
