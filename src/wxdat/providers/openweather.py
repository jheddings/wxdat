"""Weather station and data models for OpenWeatherMap.

Documentation: https://openweathermap.org/api

The data model for OpenWeatherMap is somewhat complicated and not consistent
across API calls.  Because of this, there are several similar objects to parse
data from various API endpoints.
"""

import logging
from datetime import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, Field
from wamu import Fahrenheit, Hectopascal, Meter, MilesPerHour

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


class API_Coordinates(BaseModel):
    lat: float
    lon: float


class API_Wind(BaseModel):
    deg: int
    speed: Union[int, float]
    gust: Optional[float] = None


class API_HourlyPrecip(BaseModel):
    hour1: Optional[float] = Field(alias="1h", default=None)
    hour3: Optional[float] = Field(alias="3h", default=None)


class API_Clouds(BaseModel):
    all: int


class API_City(BaseModel):
    id: int

    name: str
    country: str
    coord: API_Coordinates

    sunrise: Optional[int] = None
    sunset: Optional[int] = None


class API_WeatherNotes(BaseModel):
    id: int
    main: str
    description: str
    icon: Optional[str] = None


# https://openweathermap.org/current
class API_CurrentWeather(BaseModel):
    dt: datetime
    id: int
    name: str
    timezone: int
    coord: API_Coordinates

    main: API_Main
    wind: API_Wind
    clouds: API_Clouds
    visibility: int

    rain: Optional[API_HourlyPrecip] = None
    snow: Optional[API_HourlyPrecip] = None

    dt_txt: Optional[datetime] = None
    weather: Optional[List[API_WeatherNotes]] = None

    @property
    def remarks(self):
        if self.weather is None or len(self.weather) < 1:
            return None

        wx = self.weather[0]

        return f"{wx.main}: {wx.description} [{wx.id}]"


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
    def observe(self) -> CurrentConditions:
        conditions = self._api_get_current_weather()

        if conditions is None:
            return None

        main = conditions.main
        wind = conditions.wind

        # read fields using correct units
        temperature = Fahrenheit(main.temp)
        feels_like = Fahrenheit(main.feels_like)
        wind_speed = MilesPerHour(wind.speed)
        wind_gust = MilesPerHour(wind.gust)
        abs_pressure = Hectopascal(main.grnd_level)
        rel_pressure = Hectopascal(main.sea_level)
        visibility = Meter(conditions.visibility)

        return CurrentConditions(
            timestamp=conditions.dt,
            provider=self.provider,
            station_id=self.station_id,
            temperature=temperature.fahrenheit,
            feels_like=feels_like.fahrenheit,
            wind_speed=wind_speed.miles_per_hr,
            wind_gusts=wind_gust.miles_per_hr,
            wind_bearing=wind.deg,
            humidity=main.humidity,
            abs_pressure=abs_pressure.inches_mercury,
            rel_pressure=rel_pressure.inches_mercury,
            cloud_cover=conditions.clouds.all,
            visibility=visibility.miles,
            remarks=conditions.remarks,
        )

    def _api_get_current_weather(self) -> API_CurrentWeather:
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
        return API_CurrentWeather.model_validate(data)
