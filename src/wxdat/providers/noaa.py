"""Weather station and data models for National Weather Service (NOAA).

https://www.weather.gov/documentation/services-web-api
"""

import logging
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel
from wamu import Celsius, Meter, MetersPerSecond, Millimeter, Pascal

from ..database import CurrentConditions, HourlyForecast
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_BASE = "https://api.weather.gov/stations/"


class API_Geometry(BaseModel):
    type: str
    coordinates: List[float]


class API_Measurement(BaseModel):
    unitCode: str
    qualityControl: str
    value: Optional[float] = None


class API_Properties(BaseModel):
    station: str
    timestamp: datetime

    temperature: Optional[API_Measurement] = None
    dewpoint: Optional[API_Measurement] = None

    windDirection: Optional[API_Measurement] = None
    windSpeed: Optional[API_Measurement] = None
    windGust: Optional[API_Measurement] = None

    barometricPressure: Optional[API_Measurement] = None
    seaLevelPressure: Optional[API_Measurement] = None
    visibility: Optional[API_Measurement] = None

    precipitationLastHour: Optional[API_Measurement] = None
    relativeHumidity: Optional[API_Measurement] = None
    windChill: Optional[API_Measurement] = None
    heatIndex: Optional[API_Measurement] = None

    cloudLayers: Optional[List[Any]] = None
    presentWeather: Optional[List[Any]] = None

    textDescription: Optional[str] = None
    rawMessage: Optional[str] = None

    @property
    def feels_like(self):
        if self.temperature is None or self.temperature.value is None:
            return None

        # use heat index if temp is over 70 F
        if self.temperature.value >= 21:
            return self.heatIndex.value

        # use wind chill if temp is below 61 F
        if self.temperature.value <= 16:
            return self.windChill.value

        return self.temperature.value


class API_Observation(BaseModel):
    id: str
    geometry: API_Geometry
    properties: API_Properties


class Station(BaseStation):
    def __init__(self, name, *, station):
        super().__init__(name)

        self.logger = logger.getChild("NOAA")
        self.logger.info("Created NOAA station: %s", station)

        self.station = station

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider name for this WeatherStation."""
        return WeatherProvider.NOAA

    @property
    def current_conditions(self) -> CurrentConditions:
        weather = self.get_current_weather()

        if weather is None:
            return None

        props = weather.properties

        return CurrentConditions(
            timestamp=props.timestamp,
            provider=self.provider,
            station_id=self.station,
            temperature=Celsius(props.temperature.value).degrees_fahrenheit,
            feels_like=Celsius(props.feels_like).degrees_fahrenheit,
            dew_point=Celsius(props.dewpoint.value).degrees_fahrenheit,
            wind_speed=MetersPerSecond(props.windSpeed.value).miles_per_hr,
            wind_gusts=MetersPerSecond(props.windGust.value).miles_per_hr,
            wind_bearing=props.windDirection.value,
            humidity=props.relativeHumidity.value,
            precip_hour=Millimeter(props.precipitationLastHour.value).inches,
            abs_pressure=Pascal(props.barometricPressure.value).inches_mercury,
            rel_pressure=Pascal(props.seaLevelPressure.value).inches_mercury,
            visibility=Meter(props.visibility.value).miles,
            remarks=props.rawMessage,
        )

    @property
    def hourly_forecast(self) -> List[HourlyForecast]:
        """Return the hourly forecast for this WeatherStation."""
        return None

    def get_current_weather(self) -> API_Observation:
        self.logger.debug("getting current weather")

        url = f"{API_BASE}/{self.station}/observations/latest"

        headers = {"Accept": "application/geo+json"}

        resp = self.safer_get(url, headers=headers)

        if resp is None:
            return None

        data = resp.json()

        return API_Observation.model_validate(data)
