"""Weather station and data models for National Weather Service (NOAA).

https://www.weather.gov/documentation/services-web-api
"""

import logging
from collections.abc import Callable
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from wamu import (
    Celsius,
    KilometersPerHour,
    Meter,
    MetersPerSecond,
    MillimetersPerHour,
    Pascal,
)

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


# Conversions from the units the API may report to the units we store, keyed by the
# `unitCode` carried on each measurement.  The API declares its units per-field, so we
# convert from what it says rather than assuming.
FAHRENHEIT = {
    "wmoUnit:degC": lambda value: Celsius(value).fahrenheit,
}

MILES_PER_HOUR = {
    "wmoUnit:km_h-1": lambda value: KilometersPerHour(value).miles_per_hr,
    "wmoUnit:m_s-1": lambda value: MetersPerSecond(value).miles_per_hr,
}

INCHES_MERCURY = {
    "wmoUnit:Pa": lambda value: Pascal(value).inches_mercury,
}

MILES = {
    "wmoUnit:m": lambda value: Meter(value).miles,
}

# the API reports accumulation over the preceding hour, which we store as a rate
INCHES_PER_HOUR = {
    "wmoUnit:mm": lambda value: MillimetersPerHour(value).inches_per_hour,
}


def convert(
    measurement: API_Measurement | None,
    units: dict[str, Callable[[float], float]],
) -> float | None:
    """Convert a measurement to our storage units, using the unit the API declared."""

    if measurement is None or measurement.value is None:
        return None

    convert_from = units.get(measurement.unitCode)

    # an unrecognized unit means the API is reporting something we have not been told
    # how to read -- drop the field rather than record a value scaled by the wrong factor
    if convert_from is None:
        logger.warning("unsupported unitCode '%s'; dropping value", measurement.unitCode)
        return None

    return convert_from(measurement.value)


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
    def feelsLike(self) -> API_Measurement | None:
        """Return the measurement that best represents the apparent temperature."""

        temp = convert(self.temperature, FAHRENHEIT)

        if temp is None:
            return None

        # use heat index if temp is over 70 F
        if temp >= 70:
            return self.heatIndex

        # use wind chill if temp is below 61 F
        if temp <= 61:
            return self.windChill

        return self.temperature


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

        return CurrentConditions(
            timestamp=props.timestamp,
            provider=self.provider,
            station_id=self.station,
            temperature=convert(props.temperature, FAHRENHEIT),
            feels_like=convert(props.feelsLike, FAHRENHEIT),
            dew_point=convert(props.dewpoint, FAHRENHEIT),
            wind_speed=convert(props.windSpeed, MILES_PER_HOUR),
            wind_gusts=convert(props.windGust, MILES_PER_HOUR),
            wind_bearing=props.windDirection.value,
            humidity=props.relativeHumidity.value,
            precip_hour=convert(props.precipitationLastHour, INCHES_PER_HOUR),
            abs_pressure=convert(props.barometricPressure, INCHES_MERCURY),
            rel_pressure=convert(props.seaLevelPressure, INCHES_MERCURY),
            visibility=convert(props.visibility, MILES),
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
