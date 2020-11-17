# encapsulate main objects

import re
import logging
import time

from datetime import timedelta
from prometheus_client import Gauge

import stations

MONITOR_INTERVAL_SEC = 60

# TODO group units by category (e.g. imperial or metric)
# should there be a separate unit.py file?

# temperature units
CELCIUS = 'C'
KELVIN = 'K'
FAHRENHEIT = 'F'

# speed units
MPH = 'mph'
KPH = 'km/h'

# pressure units
INCHES_MERCURY = 'inHg'
MILLIBARS = 'mb'
KILOPASCAL = 'kPa'

# length units
INCHES = 'in'
FEET = 'ft'
MILES = 'mi'
CENTIMETERS = 'cm'
METERS = 'm'
KILOMETERS = 'km'

################################################################################
def parse_duration(value):
    # long form...
    match = re.match(r'((\d+):)?(\d+):(\d+)', value)
    if match:
        hours = match.group(2) or 0
        minutes = match.group(3) or 0
        seconds = match.group(4) or 0
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    # short form...
    match = re.match(r'((\d+)h\s*)?((\d+)m\s*)?((\d+)s)?', value)
    if match:
        hours = match.group(2) or 0
        minutes = match.group(4) or 0
        seconds = match.group(6) or 0
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))

    raise ValueError('Invalid duration: %s' % value)

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
                time.sleep(MONITOR_INTERVAL_SEC)

        except KeyboardInterrupt:
            self.logger.debug('canceled by user')

        self.logger.debug('exiting run loop')

    #---------------------------------------------------------------------------
    def _run_loop_step(self):
        self.logger.debug('updating all stations')

        for station in self.stations:
            if station.is_current:
                self.logger.debug('station %s is up to date; skipping', station.name)
            else:
                self.logger.debug('station %s is out of date; updating', station.name)
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
        # TODO support metric_prefix from global config
        safe_name = re.sub('[^a-zA-Z0-9]+', '_', self.name)
        metric_name = f'wx_{safe_name}_{gauge_name}'
        gauge = self.gauges.get(metric_name, None)

        labels = {
            'name' : self.name
        }

        if units is not None:
            labels['units'] = units

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

        if metric == 'dewPoint':
            return 'Dew Point'

        if metric == 'precipitation':
            return 'Total Precipitation'

        return 'Unknown'

    #---------------------------------------------------------------------------
    def export(self, data, *objects):
        for obj in objects:
            # parse the tuple...
            name = obj[0]
            src = obj[1]
            units = obj[2]

            # update gauges accordingly...
            if src in data and data[src] is not None:
                value = data[src]
                self.logger.debug('exporting data: %s :: data[%s] => %s', name, src, value)
                self._update_gauge(name, value, units)
            else:
                self.logger.warning('Empty source data: %s', src)

    #---------------------------------------------------------------------------
    def set_temperature(self, value, units=FAHRENHEIT):
        self._update_gauge('temperature', value, units)

    #---------------------------------------------------------------------------
    def set_dew_point(self, value, units=FAHRENHEIT):
        self._update_gauge('dewPoint', value, units)

    #---------------------------------------------------------------------------
    def set_wind_speed(self, value, units=MPH):
        self._update_gauge('windSpeed', value, units)

    #---------------------------------------------------------------------------
    def set_wind_gust(self, value, units=MPH):
        self._update_gauge('windGust', value, units)

    #---------------------------------------------------------------------------
    def set_wind_heading(self, value):
        self._update_gauge('windHeading', value)

    #---------------------------------------------------------------------------
    def set_humidity(self, value):
        self._update_gauge('humidity', value)

    #---------------------------------------------------------------------------
    def set_pressure(self, value, units=INCHES_MERCURY):
        self._update_gauge('pressure', value, units)

    #---------------------------------------------------------------------------
    def set_precipitation(self, value, units=INCHES):
        self._update_gauge('precipitation', value, units)
