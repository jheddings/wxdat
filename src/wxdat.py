# encapsulate main objects

import logging
import time

from prometheus_client import Gauge

import stations

LOOP_INTERVAL = 30

# temperature units
CELCIUS = 'C'
KELVIN = 'K'
FAHRENHEIT = 'F'

# speed units
MPH = 'mph'
KPH = 'km/h'

# pressure units
HG = 'Hg'
MB = 'mb'

################################################################################
class Monitor(object):

    stations = list()

    #---------------------------------------------------------------------------
    def __init__(self):
        self.logger = logging.getLogger('wxdat.Updater')

    #---------------------------------------------------------------------------
    def add_station(self, station):
        self.stations.append(station)

    #---------------------------------------------------------------------------
    def run(self):
        if len(self.stations) == 0:
            self.logger.warn('No stations have been configured; nothing to do')
            return

        try:
            self.logger.debug('entering run loop')

            while True:
                self._run_loop_step()
                time.sleep(LOOP_INTERVAL)

        except KeyboardInterrupt:
            self.logger.debug('canceled by user')

        self.logger.debug('exiting run loop')

    #---------------------------------------------------------------------------
    def _run_loop_step(self):
        self.logger.debug('updating all stations')
        for station in self.stations:

            # TODO check station update interval before calling...
            station.update()

################################################################################
class WeatherData(object):

    #---------------------------------------------------------------------------
    def __init__(self, name):
        self.logger = logging.getLogger('wxdat.WeatherData')
        self.gauges = dict()
        self.name = name

    #---------------------------------------------------------------------------
    def _update_gauge(self, gauge_name, value, units=None):
        metric_name = f'wx_{self.name}_{gauge_name}'
        gauge = self.gauges.get(metric_name, None)

        labels = {
            'units' : units
        }

        if gauge is None:
            self.logger.debug('building gauge: %s', metric_name)
            desc = self.describe(gauge_name)
            gauge = Gauge(metric_name, desc, labels.keys())
            self.gauges[metric_name] = gauge

        self.logger.debug('set %s => %s', metric_name, value)
        gauge.labels(**labels).set(value)

    #---------------------------------------------------------------------------
    def describe(self, metric):
        if metric == 'temperature':
            return 'Temperature'

        if metric == 'windSpeed':
            return 'Wind Speed'

        if metric == 'windGust':
            return 'Wind Gust'

        if metric == 'windHeading':
            return 'Wind Heading'

        if metric == 'humidity':
            return 'Relative Humidity'

        if metric == 'pressure':
            return 'Atmospheric Pressure'

        return 'Unknown'

    #---------------------------------------------------------------------------
    def set_temperature(self, value, units=FAHRENHEIT):
        self._update_gauge('temperature', value, units)

    #---------------------------------------------------------------------------
    def set_wind_speed(self, value, units=MPH):
        self._update_gauge('windSpeed', value, units)

    #---------------------------------------------------------------------------
    def set_wind_gust(self, value, units=MPH):
        self._update_gauge('windGust', value, units)

    #---------------------------------------------------------------------------
    def set_wind_direction(self, value):
        self._update_gauge('windHeading', value)

    #---------------------------------------------------------------------------
    def set_humidity(self, value):
        self._update_gauge('humidity', value)

    #---------------------------------------------------------------------------
    def set_pressure(self, value, units=HG):
        self._update_gauge('pressure', value, units)
