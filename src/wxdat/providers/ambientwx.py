"""Weather station and data models for Ambient Weather Network.

https://ambientweather.docs.apiary.io/
"""

import logging
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, parse_obj_as

from ..database import CurrentConditions, HourlyForecast
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://rt.ambientweather.net/v1"


# https://github.com/ambient-weather/api-docs/wiki/Device-Data-Specs
class API_DeviceData(BaseModel):
    dateutc: int
    date: datetime

    winddir: Optional[float] = None
    windspeedmph: Optional[float] = None
    windgustmph: Optional[float] = None
    windgustdir: Optional[float] = None

    maxdailygust: Optional[float] = None

    winddir_avg2m: Optional[float] = None
    windspdmph_avg2m: Optional[float] = None

    winddir_avg10m: Optional[float] = None
    windspdmph_avg10m: Optional[float] = None

    tempf: Optional[float] = None
    feelsLike: Optional[float] = None
    dewPoint: Optional[float] = None
    humidity: Optional[float] = None

    baromrelin: Optional[float] = None
    baromabsin: Optional[float] = None

    hourlyrainin: Optional[float] = None
    dailyrainin: Optional[float] = None
    weeklyrainin: Optional[float] = None
    monthlyrainin: Optional[float] = None
    yearlyrainin: Optional[float] = None
    eventrainin: Optional[float] = None
    totalrainin: Optional[float] = None

    uv: Optional[float] = None

    tempinf: Optional[float] = None
    humidityin: Optional[float] = None
    feelsLikein: Optional[float] = None
    dewPointin: Optional[float] = None

    solarradiation: Optional[float] = None


class API_DeviceDataList(BaseModel):
    __root__: List[API_DeviceData]


class Station(BaseStation):
    def __init__(self, name, *, app_key, user_key, device_id):
        super().__init__(name)

        self.logger = logger.getChild("AmbientWeather")
        self.logger.info("Created AmbientWeather station")

        self.app_key = app_key
        self.user_key = user_key
        self.device_id = device_id

    @property
    def provider(self) -> WeatherProvider:
        """Return the provider for this WeatherStation."""
        return WeatherProvider.AMBIENT

    @property
    def current_conditions(self) -> CurrentConditions:
        conditions = self.get_current_weather()

        if conditions is None:
            return None

        return CurrentConditions(
            timestamp=conditions.date,
            provider=self.provider,
            station_id=self.device_id,
            temperature=conditions.tempf,
            feels_like=conditions.feelsLike,
            wind_speed=conditions.windspeedmph,
            wind_gusts=conditions.windgustmph,
            wind_bearing=conditions.winddir,
            humidity=conditions.humidity,
            dew_point=conditions.dewPoint,
            precip_hour=conditions.hourlyrainin,
            precip_day=conditions.dailyrainin,
            precip_week=conditions.weeklyrainin,
            precip_month=conditions.monthlyrainin,
            precip_year=conditions.yearlyrainin,
            precip_total=conditions.totalrainin,
            rel_pressure=conditions.baromrelin,
            abs_pressure=conditions.baromabsin,
            solar_rad=conditions.solarradiation,
            uv_index=conditions.uv,
        )

    @property
    def hourly_forecast(self) -> List[HourlyForecast]:
        """Return the hourly forecast for this WeatherStation."""
        return None

    def get_current_weather(self) -> API_DeviceData:
        self.logger.debug("getting current weather")

        url = f"{API_ENDPOINT}/devices/{self.device_id}"

        params = {
            "apiKey": self.user_key,
            "applicationKey": self.app_key,
            "limit": 1,
        }

        resp = self.safer_get(url, params)

        if resp is None:
            return None

        data = resp.json()
        data_list = parse_obj_as(List[API_DeviceData], data)

        return data_list[0] if len(data_list) > 0 else None
