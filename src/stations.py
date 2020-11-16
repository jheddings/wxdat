# supported sensors for brewdat

import re
import logging
import requests

import wxdat

# TODO support station units
# TODO implement update_interval

################################################################################
def configure(conf):
    import importlib

    station_type = conf.pop('type')
    module = importlib.import_module('stations')
    cls = getattr(module, station_type)

    return cls(**conf)

################################################################################
class BaseStation(object):

    #---------------------------------------------------------------------------
    def __init__(self, name):
        self.logger = logging.getLogger('wxdat.stations.BaseStation')

        self.logger.debug('new station: %s', name)
        self.wxdat = wxdat.WeatherData(name)

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
        resp = requests.get(data_url)

        # TODO watch for errors

        wx = resp.json()

        if 'currently' not in wx:
            self.logger.warning('Observation error')
            return None

        return wx['currently']

    #---------------------------------------------------------------------------
    def update(self):
        current_wx = self._current_wx()

        if current_wx is None:
            self.logger.warning('Could not read current weather')
            return

        self.logger.debug('updating station weather @ %s', current_wx['time'])

        self.wxdat.set_temperature(current_wx['temperature'], units=wxdat.FAHRENHEIT)
        self.wxdat.set_dew_point(current_wx['dewPoint'], units=wxdat.FAHRENHEIT)
        self.wxdat.set_humidity(current_wx['humidity'])
        self.wxdat.set_pressure(current_wx['pressure'], units=wxdat.INCHES_MERCURY)
        self.wxdat.set_wind_heading(current_wx['windBearing'])
        self.wxdat.set_wind_speed(current_wx['windSpeed'], units=wxdat.MPH)
        self.wxdat.set_wind_gust(current_wx['windGust'], units=wxdat.MPH)

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
        resp = requests.get(data_url)

        # TODO watch for errors

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

        if current_wx is None:
            self.logger.warning('Could not read current weather')
            return

        self.logger.debug('updating station weather @ %s', current_wx['obsTimeLocal'])

        self.wxdat.set_humidity(current_wx['humidity'])
        self.wxdat.set_wind_heading(current_wx['winddir'])

        if 'imperial' in current_wx:
            obs = current_wx['imperial']
            self.wxdat.set_temperature(obs['temp'], units=wxdat.FAHRENHEIT)
            self.wxdat.set_wind_speed(obs['windSpeed'], units=wxdat.MPH)
            self.wxdat.set_wind_gust(obs['windGust'], units=wxdat.MPH)
            self.wxdat.set_pressure(obs['pressure'], units=wxdat.INCHES_MERCURY)
            self.wxdat.set_dew_point(obs['dewpt'], units=wxdat.FAHRENHEIT)
        else:
            self.logger.warning('Could not read current weather details')

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
        resp = requests.get(data_url)

        # TODO watch for errors

        return resp.json()

    #---------------------------------------------------------------------------
    def update(self):
        current_wx = self._current_wx()

        if current_wx is None:
            self.logger.warning('Could not read current weather')
            return

        self.logger.debug('updating station weather @ %s', current_wx['dt'])

        wx_main = current_wx['main']
        self.wxdat.set_temperature(wx_main['temp'], units=wxdat.FAHRENHEIT)
        self.wxdat.set_humidity(wx_main['humidity'])
        self.wxdat.set_pressure(wx_main['pressure'], units=wxdat.INCHES_MERCURY)

        wx_wind = current_wx['wind']
        self.wxdat.set_wind_heading(wx_wind['deg'])
        self.wxdat.set_wind_speed(wx_wind['speed'], units=wxdat.MPH)

