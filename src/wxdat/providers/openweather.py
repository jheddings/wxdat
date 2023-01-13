"""Weather station and data models for OpenWeatherMap.

Documentation: https://openweathermap.org/api

The data model for OpenWeatherMap is somewhat complicated and not consistent
across API calls.  Because of this, there are several similar objects to parse
data from various API endpoints.
"""

import logging
from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field

from .. import units
from ..database import CurrentConditions, HourlyForecast
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_CURRENT_WX = "https://api.openweathermap.org/data/2.5/weather"
API_DAILY_FORECAST = "https://api.openweathermap.org/data/2.5/forecast/daily"
API_HOURLY_FORECAST = "https://pro.openweathermap.org/data/2.5/forecast/hourly"
API_3HOUR_FORECAST = "https://api.openweathermap.org/data/2.5/forecast"
API_ONECALL = "https://api.openweathermap.org/data/3.0/onecall"


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
    speed: int
    gust: Optional[float] = None


class API_HourlyPrecip(BaseModel):
    hour1: Optional[float] = Field(alias="1h")
    hour3: Optional[float] = Field(alias="3h")


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


class WeatherNotesMixin:
    weather: Optional[List[API_WeatherNotes]] = None

    @property
    def remarks(self):
        if self.weather is None or len(self.weather) < 1:
            return None

        wx = self.weather[0]

        return f"{wx.main}: {wx.description} [{wx.id}]"


class API_DailyTemperature(BaseModel):
    min: float
    max: float

    morn: float
    day: float
    eve: float
    night: float


class API_DailyWeather(BaseModel, WeatherNotesMixin):
    dt: datetime

    sunrise: int
    sunset: int

    temp: API_DailyTemperature

    humidity: int
    pressure: int

    speed: float
    deg: float
    gust: float

    pop: Optional[float] = None
    rain: Optional[float] = None
    snow: Optional[float] = None

    clouds: Optional[float] = None


class API_HourlyWeather(BaseModel, WeatherNotesMixin):
    dt: datetime

    main: API_Main
    wind: API_Wind
    clouds: API_Clouds
    visibility: int

    pop: Optional[float] = None
    rain: Optional[API_HourlyPrecip] = None
    snow: Optional[API_HourlyPrecip] = None

    dt_txt: Optional[datetime] = None


# https://openweathermap.org/current
class API_CurrentWeather(BaseModel, WeatherNotesMixin):
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


# https://openweathermap.org/api/hourly-forecast
class API_HourlyForecast(BaseModel):
    cnt: int
    city: API_City
    list: List[API_HourlyWeather]


# https://openweathermap.org/api/forecast16
class API_DailyForecast(BaseModel):
    cnt: int
    city: API_City
    list: List[API_DailyWeather]


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
            remarks=conditions.remarks,
        )

    @property
    def hourly_forecast(self) -> List[HourlyForecast]:
        forecast = self.get_hourly_forecast()

        if forecast is None:
            return None

        now = datetime.now(tz=timezone.utc)

        return [
            HourlyForecast(
                timestamp=hour.dt,
                origin_time=now,
                provider=self.provider,
                station_id=self.station_id,
                temperature=hour.main.temp,
                feels_like=hour.main.feels_like,
                wind_speed=hour.wind.speed,
                wind_gusts=hour.wind.gust,
                wind_bearing=hour.wind.deg,
                humidity=hour.main.humidity,
                abs_pressure=units.hPa(hour.main.grnd_level).inHg,
                rel_pressure=units.hPa(hour.main.sea_level).inHg,
                cloud_cover=hour.clouds.all,
                visibility=units.meter(hour.visibility).miles,
                remarks=hour.remarks,
            )
            for hour in forecast.list
        ]

    def get_current_weather(self) -> API_CurrentWeather:
        return self.get_wx_data(API_CurrentWeather, API_CURRENT_WX)

    def get_hourly_forecast(self) -> API_HourlyForecast:
        return self.get_wx_data(API_HourlyForecast, API_3HOUR_FORECAST)

    def get_wx_data(self, model: BaseModel, url):
        self.logger.debug("getting weather data :: %s", model)

        params = {
            "lat": self.latitude,
            "lon": self.longitude,
            "appid": self.api_key,
            "units": "imperial",
        }

        resp = self.safer_get(url, params)

        if resp is None:
            return None

        data = resp.json()
        return model.parse_obj(data)
