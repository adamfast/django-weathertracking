from django.contrib import admin
from weathertracking.models import WeatherStation, WeatherReport

class WeatherStationAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'country', 'latitude', 'longitude', 'auto_poll')
    list_filter = ('auto_poll',)
    search_fields = ('code',)

class WeatherReportAdmin(admin.ModelAdmin):
    list_display = ('station', 'observation_time', 'temperature_celsius',
        'wind_speed_kts', 'wind_direction', 'visibility_mi', 'cycle', 'sky_conditions')
    list_filter = ('station',)
    date_hierarchy = 'observation_time'


admin.site.register(WeatherStation, WeatherStationAdmin)
admin.site.register(WeatherReport, WeatherReportAdmin)
