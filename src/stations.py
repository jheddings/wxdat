# supported sensors for brewdat

import re
import logging
import sys
import requests

from datetime import datetime
from datetime import timedelta

import wxdat

# TODO support station units

################################################################################
def configure(station_conf, global_conf=None):
    # TODO add logging support here...

    # pop anything that is unknown to the constructor
    stat_type = station_conf.pop('type')
    stat_labels = station_conf.pop('labels', None)
    cfg_interval = station_conf.pop('update_interval', None)

    # load the class from the current symbol table...
    cls = globals().get(stat_type, None)
    if cls is None: return None

    # instantiate the station using kwargs from the config...
    station = cls(**station_conf)

    # check for a global value if the local value is empty
    if cfg_interval is None and global_conf is not None:
        cfg_interval = global_conf.get('update_interval', None)

    # default to a conservative value if needed
    if cfg_interval is None:
        cfg_interval = '30m'

    # here we can directly set the update interval for our station
    station.update_interval = wxdat.parse_duration(cfg_interval)

    return station

################################################################################
class BaseStation(object):

    #---------------------------------------------------------------------------
    def __init__(self, name):
        self.logger = logging.getLogger('wxdat.stations.BaseStation')
        self.logger.debug('new station: %s', name)

        self.name = name

        # subclasses should set this to datetime.now() upon successful update
        self.last_update = None

        # we are intentionally making the default very conservative here...
        self.update_interval = timedelta(minutes=30)

        # shared data object which contains the gauges to be exported
        self.wxdat = wxdat.WeatherData(name)

    #---------------------------------------------------------------------------
    @property
    def is_current(self):
        if self.last_update is None:
            return False

        now = datetime.now()
        delta = now - self.last_update

        self.logger.debug('station %s last updated at %s (%s ago)',
                          self.name, self.last_update, delta)

        return (delta <= self.update_interval)

    #---------------------------------------------------------------------------
    def safe_get(self, url):
        # XXX may want to disable this since API keys are often in the URL...
        self.logger.debug('download %s', url)

        resp = None

        try:
            resp = requests.get(url)
            self.logger.debug('=> HTTP %d: %s', resp.status_code, resp.reason)

            # TODO watch for specific exceptions...
        except:
            self.logger.error('Error downloading data: %s', sys.exc_info()[0])
            resp = None

        if resp is None or not resp.ok:
            self.logger.warning('Could not download data')

        return resp

################################################################################
class DarkSky(BaseStation):

    #---------------------------------------------------------------------------
    def __init__(self, name, *, api_key, latitude, longitude):
        BaseStation.__init__(self, name)

        self.logger = logging.getLogger('wxdat.stations.DarkSky')
        self.logger.info('Created DarkSky station: [%s, %s]', latitude, longitude)

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude

    #---------------------------------------------------------------------------
    def _current_wx(self):
        self.logger.debug('getting current weather')
        data_url = f'https://api.darksky.net/forecast/{self.api_key}/{self.latitude},{self.longitude}'

        resp = self.safe_get(data_url)
        if resp is None: return None

        wx = resp.json()

        if 'currently' not in wx:
            self.logger.warning('Observation error')
            return None

        return wx['currently']

    #---------------------------------------------------------------------------
    def update(self):
        current_wx = self._current_wx()
        if current_wx is None: return

        self.logger.debug('updating station weather @ %s', current_wx['time'])

        self.wxdat.export(current_wx,
            ('temperature',  'temperature',        wxdat.FAHRENHEIT),
            ('dewPoint',     'dewPoint',           wxdat.FAHRENHEIT),
            ('humidity',     'humidity',           None),
            ('windHeading',  'windBearing',        None),
            ('windSpeed',    'windSpeed',          wxdat.MPH),
            ('windGust',     'windGust',           wxdat.MPH),
            ('preciptation', 'precipAccumulation', wxdat.INCHES)
        )

        self.last_update = datetime.now()

################################################################################
class WUndergroundPWS(BaseStation):

    #---------------------------------------------------------------------------
    def __init__(self, name, *, station_id, api_key):
        BaseStation.__init__(self, name)

        self.logger = logging.getLogger('wxdat.stations.WUnderground')
        self.logger.info('Created WUnderground station: %s', station_id)

        self.api_key = api_key
        self.station_id = station_id

    #---------------------------------------------------------------------------
    def _current_wx(self):
        self.logger.debug('getting current weather')
        data_url = f'https://api.weather.com/v2/pws/observations/current?apiKey={self.api_key}&stationId={self.station_id}&numericPrecision=decimal&format=json&units=e'

        resp = self.safe_get(data_url)
        if resp is None: return None

        wx = resp.json()

        if 'observations' not in wx:
            self.logger.warning('Observation error')
            return None

        if len(wx['observations']) < 1:
            self.logger.warning('Empty observations')
            return None

        obs = wx['observations']

        return obs[0]

    #---------------------------------------------------------------------------
    def update(self):
        current_wx = self._current_wx()
        if current_wx is None: return

        self.logger.debug('updating station weather @ %s', current_wx['obsTimeLocal'])

        self.wxdat.export(current_wx,
            ('humidity',    'humidity', None),
            ('windHeading', 'winddir',  None),
        )

        if 'imperial' in current_wx:
            self.wxdat.export(current_wx['imperial'],
                ('temperature',  'temp',        wxdat.FAHRENHEIT),
                ('dewPoint',     'dewpt',       wxdat.FAHRENHEIT),
                ('pressure',     'pressure',    wxdat.INCHES_MERCURY),
                ('windSpeed',    'windSpeed',   wxdat.MPH),
                ('windGust',     'windGust',    wxdat.MPH),
                ('preciptation', 'precipTotal', wxdat.INCHES)
            )
        else:
            self.logger.warning('Could not read current weather details')

        self.last_update = datetime.now()

################################################################################
class OpenWeather(BaseStation):

    #---------------------------------------------------------------------------
    def __init__(self, name, *, api_key, latitude, longitude):
        BaseStation.__init__(self, name)

        self.logger = logging.getLogger('wxdat.stations.OpenWeather')
        self.logger.info('Created OpenWeather station: [%s, %s]', latitude, longitude)

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude

    #---------------------------------------------------------------------------
    def _current_wx(self):
        self.logger.debug('getting current weather')
        data_url = f'https://api.openweathermap.org/data/2.5/weather?lat={self.latitude}&lon={self.latitude}&appid={self.api_key}&mode=json&units=imperial'

        resp = self.safe_get(data_url)
        if resp is None: return None

        return resp.json()

    #---------------------------------------------------------------------------
    def update(self):
        current_wx = self._current_wx()
        if current_wx is None: return

        self.logger.debug('updating station weather @ %s', current_wx['dt'])

        if 'main' in current_wx:
            self.wxdat.export(current_wx['main'],
                ('temperature', 'temp',     wxdat.FAHRENHEIT),
                ('pressure',    'pressure', wxdat.INCHES_MERCURY),
                ('humidity',    'humidity', None)
            )
        else:
            self.logger.warning('Could not read current weather details')

        if 'wind' in current_wx:
            self.wxdat.export(current_wx['wind'],
                ('windHeading', 'deg',   None),
                ('windSpeed',   'speed', wxdat.MPH)
            )
        else:
            self.logger.warning('Could not read current wind details')

        self.last_update = datetime.now()
