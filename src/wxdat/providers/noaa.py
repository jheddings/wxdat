"""Weather station and data models for National Weather Service (NOAA).

https://www.weather.gov/documentation/services-web-api
"""

import logging
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel

from .. import units
from ..database import CurrentConditions
from . import WeatherStation

logger = logging.getLogger(__name__)

API_BASE = "https://api.weather.gov/stations/"


class API_Geometry(BaseModel):
    type: str
    coordinates: List[int]


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


class Station(WeatherStation):
    def __init__(self, name, *, station):
        super().__init__(name)

        self.logger = logger.getChild("NOAA")
        self.logger.info("Created NOAA station: %s", station)

        self.station = station

    @property
    def provider_name(self):
        """Return the provider name for this WeatherStation."""
        return "NOAA"

    @property
    def current_conditions(self) -> CurrentConditions:
        weather = self.get_current_weather()

        if weather is None:
            return None

        props = weather.properties

        return CurrentConditions(
            timestamp=props.timestamp,
            provider=self.provider_name,
            station_id=self.station,
            temperature=units.degC__degF(props.temperature.value),
            feels_like=units.degC__degF(props.feels_like),
            dew_point=units.degC__degF(props.dewpoint.value),
            wind_speed=units.mps__mph(props.windSpeed.value),
            wind_gusts=units.mps__mph(props.windGust.value),
            wind_bearing=props.windDirection.value,
            humidity=props.relativeHumidity.value,
            precip_hour=units.mm__in(props.precipitationLastHour.value),
            abs_pressure=units.Pa__inHg(props.barometricPressure.value),
            rel_pressure=units.Pa__inHg(props.seaLevelPressure.value),
            visibility=units.meter__mile(props.visibility.value),
            remarks=props.rawMessage,
        )

    def get_current_weather(self) -> API_Observation:
        self.logger.debug("getting current weather")

        url = f"{API_BASE}/{self.station}/observations/latest"

        headers = {"Accept": "application/geo+json"}

        resp = self.safe_get(url, headers=headers)

        if resp is None:
            return None

        data = resp.json()

        return API_Observation.parse_obj(data)
