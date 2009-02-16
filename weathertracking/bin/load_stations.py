import csv
from decimal import Decimal
from django.contrib.gis.geos import Point
from weathertracking.models import WeatherStation

# get the nsd_cccc.txt file from http://weather.noaa.gov/tg/site.shtml and set the path to it below
# note that in the version of this file I downloaded I had to change a (letter) O in the station longitude of station KTXK to a zero.
# I emailed NOAA about it, but if they don't fix it and you get a single fail on the decimal conversion, that's what the issue is.
NOAA_FILE = 'nsd_cccc.txt'

def convert_faa_coordinate(value):
    direction = ''
    if value:
        if value[-1] == 'N' or value[-1] == 'E' or value[-1] == 'S' or value[-1] == 'W':
            direction = value[-1]
            value = value[:-1]

        value = value.split('-')
        degrees = Decimal(value[0])
        minutes = Decimal(value[1])
        try:
            seconds = Decimal(value[2])
        except: # they don't always provide seconds
            seconds = Decimal('0.0')

        overall = (degrees + (minutes / 60) + (seconds / 3600))
        if direction == 'S' or direction == 'W':
            overall = overall * -1

        return overall
    else:
        return 0.0

def import_stations():
    reader = csv.reader(open(NOAA_FILE, 'rU'), delimiter=';', quoting=csv.QUOTE_MINIMAL)

    for row in reader:
        station = WeatherStation.objects.get_or_create(code=row[0])[0]
        station.name = row[3]
        station.state = row[4][:2]
        station.country = row[5]
        try:
            station.latitude = convert_faa_coordinate(row[7])
        except:
            print 'Failed Decimal conversion (latitude) (station %s):' % (row[7], row[0])
        try:
            station.longitude = convert_faa_coordinate(row[8])
        except:
            print 'Failed Decimal conversion (longitude) (station %s): %s' % (row[8], row[0])
        if station.latitude and station.longitude:
            station.point = Point((station.longitude, station.latitude),)
        if row[11]:
            station.elevation = row[11]
        station.save()


if __name__ == '__main__':
    import_stations()
