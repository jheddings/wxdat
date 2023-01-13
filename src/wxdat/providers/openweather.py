"""Weather station and data models for OpenWeatherMap.

https://openweathermap.org/api
"""

import logging
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

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


class API_Rain(BaseModel):
    three_hour: float = Field(alias="3h")


class API_Snow(BaseModel):
    three_hour: float = Field(alias="3h")


class API_Clouds(BaseModel):
    all: int


class API_Conditions(BaseModel):
    dt: datetime
    clouds: API_Clouds
    main: API_Main

    wind: API_Wind
    clouds: API_Clouds
    visibility: int

    rain: Optional[API_Rain] = None
    snow: Optional[API_Snow] = None

    weather: Optional[List[API_Notes]] = None

    dt_txt: Optional[datetime] = None

    @property
    def description(self):
        if self.weather is None or len(self.weather) < 1:
            return None

        wx = self.weather[0]

        return f"{wx.main}: {wx.description} [{wx.id}]"


class API_City(BaseModel):
    id: int

    name: str
    country: str

    sunrise: int
    sunset: int

    coord: API_Coordinates


# https://openweathermap.org/current
class API_Weather(API_Conditions):
    id: int
    name: str
    coord: API_Coordinates


# https://openweathermap.org/api/hourly-forecast
class API_HourlyForecast(BaseModel):
    cnt: int
    city: API_City
    list: List[API_Conditions]


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

        main = conditions.main
        wind = conditions.wind

        return CurrentConditions(
            timestamp=conditions.dt,
            provider=self.provider,
            station_id=self.station_id,
            temperature=main.temp,
            feels_like=main.feels_like,
            wind_speed=wind.speed,
            wind_gusts=wind.gust,
            wind_bearing=wind.deg,
            humidity=main.humidity,
            abs_pressure=units.hPa(main.grnd_level).inHg,
            rel_pressure=units.hPa(main.sea_level).inHg,
            cloud_cover=conditions.clouds.all,
            visibility=units.meter(conditions.visibility).miles,
            remarks=conditions.description,
        )

    def get_current_weather(self) -> API_Weather:
        self.logger.debug("getting current weather")

        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": self.api_key,
            "units": "imperial",
        }

        resp = self.safer_get(API_CURRENT_WX, params)

        if resp is None:
            return None

        data = resp.json()
        return API_Weather.parse_obj(data)
