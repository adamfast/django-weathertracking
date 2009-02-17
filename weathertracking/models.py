from django.contrib.gis.db import models
from metar.Metar import Metar # available from http://homepage.mac.com/wtpollard/Software/FileSharing4.html

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
    timestamp = models.DateTimeField(auto_now_add=True) # keep track of when it was retrieved - necessary because METARs don't include any month/year info

    # denormalized data - obtainable by parsing the raw info, but stored for convenience of lookup
    observation_type = models.CharField(max_length=5, null=True, blank=True) # METAR or SPECI
    observation_mode = models.CharField(max_length=4, null=True, blank=True) # AUTO or COR (corrected)
    observation_cycle = models.IntegerField(null=True, blank=True) # a number between 0 and 23
    observation_time = models.DateTimeField(null=True, blank=True)
    wind_direction = models.IntegerField(null=True, blank=True)
    wind_compass = models.CharField(max_length=4, null=True, blank=True)
    wind_direction_from = models.IntegerField(null=True, blank=True) # used when the wind direction is variable and specified
    wind_direction_to = models.IntegerField(null=True, blank=True)   # ^^^
    wind_speed_kts = models.IntegerField(null=True, blank=True)
    wind_speed_gust_kts = models.IntegerField(null=True, blank=True)
    visibility_mi = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    temperature_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    temperature_fahrenheit = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dewpoint_celsius = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    dewpoint_fahrenheit = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    sky_conditions = models.TextField(null=True, blank=True)

    objects = WeatherReportManager()

    def get_metar_object(self):
        return Metar(self.raw)

    def save(self, **kwargs):
        "Populate all the denormalized data fields by using the metar class before saving."
        metar = self.get_metar_object()

        self.observation_time = metar.time
        self.observation_cycle = metar.cycle
        self.observation_type = metar.type
        self.observation_mode = metar.mod
        self.temperature_celsius = '%s' % metar.temp.value(units='c')
        self.temperature_fahrenheit = '%s' % metar.temp.value(units='f')
        self.dewpoint_celsius = '%s' % metar.dewpt.value(units='c')
        self.dewpoint_fahrenheit = '%s' % metar.dewpt.value(units='f')
        self.visibility_mi = '%s' % metar.vis.value(units='MI')
        self.wind_direction = '%s' % int(metar.wind_dir.value())
        self.wind_compass = metar.wind_dir.compass()
        if metar.wind_dir_from:
            self.wind_direction_from = '%s' % int(metar.wind_dir_from.value())
        if metar.wind_dir_to:
            self.wind_direction_to = '%s' % int(metar.wind_dir_to.value())
        self.wind_speed_kts = '%s' % int(metar.wind_speed.value()) # metars will only return integers when using kts
        if metar.wind_gust:
            self.wind_speed_gust_kts = '%s' % int(metar.wind_gust.value())
        self.sky_conditions = '%s' % metar.sky_conditions()

        super(WeatherReport, self).save(**kwargs)

    def __unicode__(self):
        return u'%s' % self.raw
