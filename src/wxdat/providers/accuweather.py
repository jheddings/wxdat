"""Weather station and data models for AccuWeather.

https://developer.accuweather.com/apis
"""

import logging
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, parse_obj_as

from ..database import CurrentConditions, HourlyForecast
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_CURRENT_WX = "http://dataservice.accuweather.com/currentconditions/v1"


class Precipitation(str, Enum):
    RAIN = "Rain"
    SNOW = "Snow"
    ICE = "Ice"
    MIXED = "Mixed"


class API_Measurement(BaseModel):
    Value: float
    Unit: str
    Phrase: Optional[str] = None


class API_Measurements(BaseModel):
    Metric: API_Measurement
    Imperial: API_Measurement


class API_WindDirection(BaseModel):
    Degrees: float
    English: Optional[str] = None


class API_Wind(BaseModel):
    Speed: API_Measurements
    Direction: Optional[API_WindDirection] = None


class API_Precipitation(BaseModel):
    Precipitation: Optional[API_Measurements] = None
    PastHour: Optional[API_Measurements] = None
    Past3Hours: Optional[API_Measurements] = None
    Past6Hours: Optional[API_Measurements] = None
    Past9Hours: Optional[API_Measurements] = None
    Past12Hours: Optional[API_Measurements] = None
    Past18Hours: Optional[API_Measurements] = None
    Past24Hours: Optional[API_Measurements] = None


class API_Observation(BaseModel):
    EpochTime: int
    LocalObservationDateTime: datetime
    IsDayTime: Optional[bool] = None
    WeatherText: Optional[str] = None

    HasPrecipitation: Optional[bool] = None
    PrecipitationType: Optional[Precipitation] = None

    Temperature: Optional[API_Measurements] = None
    RealFeelTemperature: Optional[API_Measurements] = None
    ApparentTemperature: Optional[API_Measurements] = None
    DewPoint: Optional[API_Measurements] = None

    Wind: Optional[API_Wind] = None
    WindGust: Optional[API_Wind] = None

    UVIndex: Optional[float] = None
    RelativeHumidity: Optional[float] = None
    Pressure: Optional[API_Measurements] = None
    Visibility: Optional[API_Measurements] = None
    CloudCover: Optional[float] = None

    Precip1hr: Optional[API_Measurements] = None
    PrecipitationSummary: Optional[API_Precipitation] = None


class Station(BaseStation):
    def __init__(self, name, *, api_key, location):
        super().__init__(name)

        self.logger = logger.getChild("AccuWeather")
        self.logger.info("Created AccuWeather station: %s", location)

        self.api_key = api_key
        self.location = location

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider for this WeatherStation."""
        return WeatherProvider.ACCUWEATHER

    @property
    def current_conditions(self) -> CurrentConditions:
        weather = self.get_current_weather()

        if weather is None:
            return None

        return CurrentConditions(
            timestamp=weather.LocalObservationDateTime,
            provider=self.provider,
            station_id=self.location,
            temperature=weather.Temperature.Imperial.Value,
            feels_like=weather.RealFeelTemperature.Imperial.Value,
            dew_point=weather.DewPoint.Imperial.Value,
            wind_speed=weather.Wind.Speed.Imperial.Value,
            wind_gusts=weather.WindGust.Speed.Imperial.Value,
            wind_bearing=weather.Wind.Direction.Degrees,
            humidity=weather.RelativeHumidity,
            precip_hour=weather.Precip1hr.Imperial.Value,
            abs_pressure=weather.Pressure.Imperial.Value,
            cloud_cover=weather.CloudCover,
            visibility=weather.Visibility.Imperial.Value,
            uv_index=weather.UVIndex,
            remarks=weather.WeatherText,
        )

    @property
    def hourly_forecast(self) -> List[HourlyForecast]:
        """Return the hourly forecast for this WeatherStation."""
        return None

    def get_current_weather(self) -> API_Observation:
        self.logger.debug("getting current weather")

        url = f"{API_CURRENT_WX}/{self.location}"

        params = {
            "apikey": self.api_key,
            "details": True,
            "language": "en-US",
        }

        resp = self.safer_get(url, params)

        if resp is None:
            return None

        data = resp.json()
        data_list = parse_obj_as(List[API_Observation], data)

        return data_list[0]
