"""Weather station and data models for National Weather Service (NOAA).

https://www.weather.gov/documentation/services-web-api
"""

import logging
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from wamu import Celsius, Meter, MetersPerSecond, MillimetersPerHour, Pascal

from ..database import CurrentConditions
from . import BaseStation, WeatherObservation, WeatherProvider

logger = logging.getLogger(__name__)

API_BASE = "https://api.weather.gov/stations/"


class API_Geometry(BaseModel):
    type: str
    coordinates: list[float]


class API_Measurement(BaseModel):
    unitCode: str
    qualityControl: str
    value: float | None = None


class API_Properties(BaseModel):
    station: str
    timestamp: datetime

    temperature: API_Measurement | None = None
    dewpoint: API_Measurement | None = None

    windDirection: API_Measurement | None = None
    windSpeed: API_Measurement | None = None
    windGust: API_Measurement | None = None

    barometricPressure: API_Measurement | None = None
    seaLevelPressure: API_Measurement | None = None
    visibility: API_Measurement | None = None

    precipitationLastHour: API_Measurement | None = None
    relativeHumidity: API_Measurement | None = None
    windChill: API_Measurement | None = None
    heatIndex: API_Measurement | None = None

    cloudLayers: list[Any] | None = None
    presentWeather: list[Any] | None = None

    textDescription: str | None = None
    rawMessage: str | None = None

    @property
    def feelsLike(self):
        if self.temperature is None or self.temperature.value is None:
            return None

        temp = Celsius(self.temperature.value)

        # use heat index if temp is over 70 F
        if temp.fahrenheit >= 70:
            return self.heatIndex.value

        # use wind chill if temp is below 61 F
        if temp.fahrenheit <= 61:
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
    def observe(self) -> WeatherObservation:
        weather = self._api_get_current_weather()

        if weather is None:
            return None

        props = weather.properties

        # set up fields for conversion
        temperature = Celsius(props.temperature.value)
        feels_like = Celsius(props.feelsLike)
        dew_point = Celsius(props.dewpoint.value)
        wind_speed = MetersPerSecond(props.windSpeed.value)
        wind_gusts = MetersPerSecond(props.windGust.value)
        precip_hour = MillimetersPerHour(props.precipitationLastHour.value)
        abs_pressure = Pascal(props.barometricPressure.value)
        rel_pressure = Pascal(props.seaLevelPressure.value)
        visibility = Meter(props.visibility.value)

        return CurrentConditions(
            timestamp=props.timestamp,
            provider=self.provider,
            station_id=self.station,
            temperature=temperature.fahrenheit,
            feels_like=feels_like.fahrenheit,
            dew_point=dew_point.fahrenheit,
            wind_speed=wind_speed.miles_per_hr,
            wind_gusts=wind_gusts.miles_per_hr,
            wind_bearing=props.windDirection.value,
            humidity=props.relativeHumidity.value,
            precip_hour=precip_hour.inches_per_hour,
            abs_pressure=abs_pressure.inches_mercury,
            rel_pressure=rel_pressure.inches_mercury,
            visibility=visibility.miles,
            remarks=props.rawMessage,
        )

    def _api_get_current_weather(self) -> API_Observation:
        self.logger.debug("getting current weather")

        url = f"{API_BASE}/{self.station}/observations/latest"

        headers = {"Accept": "application/geo+json"}

        resp = self.safer_get(url, headers=headers)

        if resp is None:
            return None

        data = resp.json()

        return API_Observation.model_validate(data)
