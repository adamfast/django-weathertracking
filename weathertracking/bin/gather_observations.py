from weathertracking.models import WeatherStation, WeatherReport

if __name__ == '__main__': # called as a script
    station_list = WeatherStation.objects.auto_poll() # retrieve all stations marked to poll automatically
    for station in station_list:
        var = station.update()
