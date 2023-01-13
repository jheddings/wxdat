"""Weather station and data models for Weather Underground.

https://www.wunderground.com/weather/api
"""

import logging
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from ..database import CurrentConditions, HourlyForecast
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://api.weather.com/v2/pws/observations/current"


class API_ImperialObs(BaseModel):
    temp: Optional[float] = None
    dewpt: Optional[float] = None
    pressure: Optional[float] = None

    heatIndex: Optional[float] = None
    windChill: Optional[float] = None

    windSpeed: Optional[float] = None
    windGust: Optional[float] = None

    precipRate: Optional[float] = None
    precipTotal: Optional[float] = None

    elev: Optional[float] = None

    @property
    def feels_like(self):
        if self.temp >= 70:
            return self.heatIndex

        if self.temp <= 61:
            return self.windChill

        return self.temp


class API_Observation(BaseModel):
    stationID: str

    epoch: Optional[datetime] = None
    obsTimeUtc: Optional[datetime] = None
    obsTimeLocal: Optional[datetime] = None

    lon: Optional[float] = None
    lat: Optional[float] = None

    country: Optional[str] = None
    neighborhood: Optional[str] = None

    uv: Optional[float] = None
    solarRadation: Optional[float] = None
    humidity: Optional[float] = None

    winddir: Optional[float] = None

    imperial: Optional[API_ImperialObs] = None


class API_Current(BaseModel):
    observations: List[API_Observation] = []


class Station(BaseStation):
    def __init__(self, name, *, station_id, api_key):
        super().__init__(name)

        self.logger = logger.getChild("WUnderground")
        self.logger.info("Created WUnderground station: %s", station_id)

        self.api_key = api_key
        self.station_id = station_id

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider name for this WeatherStation."""
        return WeatherProvider.WUNDERGROUND

    @property
    def current_conditions(self) -> CurrentConditions:
        weather = self.get_current_weather()

        if weather is None:
            return None

        conditions = weather.imperial

        return CurrentConditions(
            timestamp=weather.obsTimeUtc,
            provider=self.provider,
            station_id=self.station_id,
            temperature=conditions.temp,
            feels_like=conditions.feels_like,
            wind_speed=conditions.windSpeed,
            wind_gusts=conditions.windGust,
            wind_bearing=weather.winddir,
            humidity=weather.humidity,
            dew_point=conditions.dewpt,
            abs_pressure=conditions.pressure,
            uv_index=weather.uv,
            solar_rad=weather.solarRadation,
            precip_day=conditions.precipTotal,
            precip_hour=conditions.precipRate,
        )

    @property
    def hourly_forecast(self) -> List[HourlyForecast]:
        """Return the hourly forecast for this WeatherStation."""
        return None

    def get_current_weather(self) -> API_Observation:
        self.logger.debug("getting current weather")

        params = {
            "apiKey": self.api_key,
            "stationId": self.station_id,
            "format": "json",
            "numericPrecision": "decimal",
            "units": "e",
        }

        resp = self.safer_get(API_ENDPOINT, params)

        if resp is None:
            return None

        data = resp.json()

        current = API_Current.parse_obj(data)

        if len(current.observations) < 1:
            return None

        return current.observations[0]
