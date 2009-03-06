from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
from django.test import TestCase
from weathertracking.models import WeatherStation
from weathertracking.utils import find_nearest_weather_station, find_nearest_weather_stations

class TestWeathertracking(TestCase):
    def setUp(self):
        # create a few sample weather stations
        lwc = WeatherStation(code='KLWC', point=Point(-95.2166666666666686, 39.0166666666666657)).save()
        top = WeatherStation(code='KTOP', point=Point(-95.6333333333333400, 39.0666666666666700)).save()
        foe = WeatherStation(code='KFOE', point=Point(-95.6500000000000057, 38.9333333333333300)).save()
        ixd = WeatherStation(code='KIXD', point=Point(-94.8833333333333400, 38.8166666666666700)).save()
        ojc = WeatherStation(code='KOJC', point=Point(-94.7333333333333343, 38.8333333333333357)).save()
        flv = WeatherStation(code='KFLV', point=Point(-94.9166666666666714, 39.3666666666666671)).save()
        mci = WeatherStation(code='KMCI', point=Point(-94.7333333333333343, 39.2999999999999972)).save()
        mkc = WeatherStation(code='KMKC', point=Point(-94.5999999999999943, 39.1166666666666671)).save()
        jln = WeatherStation(code='KJLN', point=Point(-94.5000000000000000, 37.1499999999999986)).save()
        cfv = WeatherStation(code='KCFV', point=Point(-95.5666666666666629, 37.0833333333333357)).save()

    def test_lawrence_nearby(self):
        office = Point(-95.286830, 38.971330)
        station = find_nearest_weather_station(office)
        self.failUnlessEqual(station.code, 'KLWC')
        self.failUnlessEqual('%s' % station.distance.mi, '4.89983560723')

    def test_joplin_nearby(self):
        jln_best_buy = Point(-94.474030, 37.093610)
        station = find_nearest_weather_station(jln_best_buy)
        self.failUnlessEqual(station.code, 'KJLN')
        self.failUnlessEqual('%s' % station.distance.mi, '4.15055339462')

    def test_lawrence_nearby_list(self):
        office = Point(-95.286830, 38.971330)
        stations = find_nearest_weather_stations(office) # will return 5
        self.failUnlessEqual(stations[0].code, u'KLWC')
        self.failUnlessEqual(stations[1].code, u'KFOE')
        self.failUnlessEqual(stations[2].code, u'KTOP')
        self.failUnlessEqual(stations[3].code, u'KIXD')
        self.failUnlessEqual(stations[4].code, u'KOJC')
