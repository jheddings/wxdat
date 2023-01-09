"""Weather station and data models for OpenWeatherMap.

TODO - URL
"""

import logging
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from .. import units
from ..database import CurrentConditions
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_CURRENT_WX = "https://api.openweathermap.org/data/2.5/weather"


class API_Main(BaseModel):
    temp: float

    humidity: int
    pressure: int

    feels_like: Optional[float] = None
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None

    sea_level: Optional[int] = None
    grnd_level: Optional[int] = None


class API_Notes(BaseModel):
    id: int
    main: str
    description: str
    icon: Optional[str] = None


class API_Coordinates(BaseModel):
    lat: float
    lon: float


class API_Wind(BaseModel):
    deg: int
    speed: int

    gust: Optional[float] = None


class API_Clouds(BaseModel):
    all: int


class API_Conditions(BaseModel):
    dt: datetime
    clouds: API_Clouds
    main: API_Main
    wind: API_Wind
    visibility: int


class API_City(BaseModel):
    id: int
    name: str
    coord: API_Coordinates
    country: str
    sunrise: int
    sunset: int


# https://openweathermap.org/current
class API_Weather(API_Conditions):
    id: int
    name: str
    coord: API_Coordinates
    weather: List[API_Notes]


# https://openweathermap.org/api/hourly-forecast
class API_HourlyForecast(BaseModel):
    cnt: int
    list: List[API_Conditions]
    city: API_City


class Station(BaseStation):
    def __init__(self, name, *, api_key, latitude, longitude):
        super().__init__(name)

        self.logger = logger.getChild("OpenWeatherMap")
        self.logger.info("Created OpenWeather station: [%s, %s]", latitude, longitude)

        self.api_key = api_key
        self.latitude = latitude
        self.longitude = longitude

        # generate a station ID for database entries
        self.station_id = f"{latitude},{longitude}"

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider name for this WeatherStation."""
        return WeatherProvider.OPENWEATHERMAP

    @property
    def current_conditions(self) -> CurrentConditions:
        conditions = self.get_current_weather()

        if conditions is None:
            return None

        # convert pressure from hPa to inHg
        pressure = conditions.main.pressure / 33.863886666667

        return CurrentConditions(
            timestamp=conditions.dt,
            provider=self.provider,
            station_id=self.station_id,
            temperature=conditions.main.temp,
            feels_like=conditions.main.feels_like,
            wind_speed=conditions.wind.speed,
            wind_gusts=conditions.wind.gust,
            wind_bearing=conditions.wind.deg,
            humidity=conditions.main.humidity,
            abs_pressure=pressure,
            cloud_cover=conditions.clouds.all,
            visibility=units.meter__mile(conditions.visibility),
        )

    def get_current_weather(self) -> API_Weather:
        self.logger.debug("getting current weather")

        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": self.api_key,
            # TODO support configured units
            "units": "imperial",
        }

        resp = self.safe_get(API_CURRENT_WX, params)

        if resp is None:
            return None

        data = resp.json()
        return API_Weather.parse_obj(data)
