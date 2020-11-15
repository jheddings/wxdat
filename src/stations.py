# supported sensors for brewdat

import re
import logging
import requests

import wxdat

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

        self.wxdat.set_pressure(current_wx['humidity'])
        self.wxdat.set_wind_direction(current_wx['winddir'])

        radiation = current_wx['solarRadiation']
        uv = current_wx['uv']

        if 'imperial' in current_wx:
            obs = current_wx['imperial']

            self.wxdat.set_temperature(obs['temp'], units=wxdat.FAHRENHEIT)
            self.wxdat.set_wind_speed(obs['windSpeed'], units=wxdat.MPH)
            self.wxdat.set_wind_gust(obs['windGust'], units=wxdat.MPH)
            self.wxdat.set_pressure(obs['pressure'], units=wxdat.HG)

            dewpt = obs['dewpt']
            precip = obs['precipTotal']

        else:
            self.logger.warning('Could not read current weather details')
