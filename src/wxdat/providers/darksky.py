"""Weather station and data models for Dark Sky.

TODO - URL
"""

import logging
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel

from .. import units
from ..database import CurrentConditions
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://api.darksky.net/forecast"


class PrecipitationType(str, Enum):
    SNOW = "snow"
    RAIN = "rain"


class API_Conditions(BaseModel):
    time: int
    summary: Optional[str] = None
    icon: Optional[str] = None

    temperature: Optional[float] = None
    apparentTemperature: Optional[float] = None
    dewPoint: Optional[float] = None

    humidity: Optional[float] = None
    pressure: Optional[float] = None

    windSpeed: Optional[float] = None
    windGust: Optional[float] = None
    windBearing: Optional[float] = None

    cloudCover: Optional[float] = None
    uvIndex: Optional[float] = None
    visibility: Optional[float] = None
    ozone: Optional[float] = None

    precipIntensity: Optional[float] = None
    precipProbability: Optional[float] = None
    nearestStormDistance: Optional[float] = None
    nearestStormBearing: Optional[float] = None

    @property
    def timestamp(self):
        return datetime.fromtimestamp(self.time)


class API_Forecast(BaseModel):
    time: int
    summary: str
    icon: Optional[str] = None

    sunriseTime: Optional[int] = None
    sunsetTime: Optional[int] = None
    moonPhase: Optional[float] = None

    precipIntensity: Optional[float] = None
    precipIntensityMax: Optional[float] = None
    precipIntensityMaxTime: Optional[int] = None
    precipProbability: Optional[float] = None
    precipType: Optional[PrecipitationType] = None

    temperatureHigh: Optional[float] = None
    temperatureHighTime: Optional[int] = None
    temperatureLow: Optional[float] = None
    temperatureLowTime: Optional[int] = None

    temperatureMin: Optional[float] = None
    temperatureMinTime: Optional[int] = None
    temperatureMax: Optional[float] = None
    temperatureMaxTime: Optional[int] = None

    windSpeed: Optional[float] = None
    windGust: Optional[float] = None
    windGustTime: Optional[int] = None
    windBearing: Optional[float] = None

    cloudCover: Optional[float] = None
    uvIndex: Optional[float] = None
    uvIndexTime: Optional[int] = None

    dewPoint: Optional[float] = None
    humidity: Optional[float] = None
    pressure: Optional[float] = None
    uvIndex: Optional[float] = None
    visibility: Optional[float] = None
    ozone: Optional[float] = None


class API_Minutely(BaseModel):
    summary: str
    icon: Optional[str] = None
    data: List[API_Conditions] = []


class API_Hourly(BaseModel):
    summary: str
    icon: Optional[str] = None
    data: List[API_Conditions] = []


class API_Daily(BaseModel):
    summary: str
    icon: Optional[str] = None
    data: List[API_Forecast] = []


class API_Flags(BaseModel):

    units: str
    sources: List[str] = []


class API_Weather(BaseModel):
    offset: float
    latitude: float
    longitude: float
    timezone: str

    currently: API_Conditions
    minutely: Optional[API_Minutely] = None
    hourly: Optional[API_Hourly] = None
    daily: Optional[API_Daily] = None
    flags: Optional[API_Flags] = None


class Station(BaseStation):
    def __init__(self, name, *, api_key, latitude, longitude):
        super().__init__(name)

        self.logger = logger.getChild("DarkSky")
        self.logger.info("Created DarkSky station: [%s, %s]", latitude, longitude)

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude

        # generate a station ID for database entries
        self.station_id = f"{latitude},{longitude}"

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider name for this WeatherStation."""
        return WeatherProvider.DARKSKY

    @property
    def current_conditions(self) -> CurrentConditions:
        weather = self.get_current_weather()

        if weather is None:
            return None

        conditions = weather.currently

        # convert pressure from hPa to inHg

        return CurrentConditions(
            timestamp=conditions.timestamp,
            provider=self.provider,
            station_id=self.station_id,
            temperature=conditions.temperature,
            feels_like=conditions.apparentTemperature,
            wind_speed=conditions.windSpeed,
            wind_gusts=conditions.windGust,
            wind_bearing=conditions.windBearing,
            humidity=conditions.humidity * 100.0,
            dew_point=conditions.dewPoint,
            abs_pressure=units.hPa(conditions.pressure).inHg,
            cloud_cover=conditions.cloudCover * 100.0,
            visibility=conditions.visibility,
            uv_index=conditions.uvIndex,
            remarks=conditions.summary,
        )

    def get_current_weather(self) -> API_Weather:
        self.logger.debug("getting current weather")

        data_url = f"{API_ENDPOINT}/{self.api_key}/{self.latitude},{self.longitude}"

        resp = self.safer_get(data_url)

        if resp is None:
            return None

        data = resp.json()

        return API_Weather.parse_obj(data)
