from django.contrib.gis.db import models

class WeatherStationManager(models.GeoManager):
    def auto_poll(self):
        return self.filter(auto_poll__exact=True)

class WeatherStation(models.Model):
    code = models.CharField(max_length=20, unique=True,
        help_text="""Station code (lower case).
        Use <a href="http://www.rap.ucar.edu/weather/surface/stations.txt">NOAA ICAO</a>
        when available or use an alternate code scheme.""")
    name = models.CharField(max_length=200, null=True, blank=True)
    name_override = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    auto_poll = models.BooleanField(default=False)
    point = models.PointField(srid=4326, null=True, blank=True)

    objects = WeatherStationManager()

    def get_name(self):
        if self.name_override:
            return self.name_override
        return self.name

    def __unicode__(self):
        return u'%s' % self.code

class WeatherReportManager(models.Manager):
    def twenty_four_newest(self):
        return self.order_by('-timestamp')[:24]
    def all(self, limit=None):
        return self.order_by('-timestamp')

class WeatherReport(models.Model):
    station = models.ForeignKey(WeatherStation)
    raw = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    observation_time = models.DateTimeField(null=True, blank=True)
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_fahrenheit = models.DecimalField(max_digits=5, decimal_places=2)
    dewpoint_celsius = models.DecimalField(max_digits=5, decimal_places=2)
    dewpoint_fahrenheit = models.DecimalField(max_digits=5, decimal_places=2)
    wind_speed_kts = models.IntegerField()
    wind_speed_meters_per_second = models.DecimalField(max_digits=10, decimal_places=7)
    wind_speed_miles_per_hour = models.DecimalField(max_digits=10, decimal_places=7)
    wind_direction = models.IntegerField(null=True, blank=True)
    wind_compass = models.CharField(max_length=4, null=True, blank=True)
    visibility_km = models.DecimalField(max_digits=10, decimal_places=7)
    visibility_mi = models.DecimalField(max_digits=10, decimal_places=7)
    humidity_percent = models.IntegerField()
    barometric_pressure_mb = models.DecimalField(max_digits=14, decimal_places=10)
    altimeter = models.DecimalField(max_digits=4, decimal_places=2)
    cycle = models.IntegerField(null=True, blank=True)
    sky_conditions = models.CharField(max_length=256)

    objects = WeatherReportManager()

    def __unicode__(self):
        return u'%s' % self.raw
