"""Weather station and data models for Ambient Weather Network.

https://ambientweather.docs.apiary.io/
"""

import logging
from datetime import datetime

from pydantic import BaseModel, TypeAdapter
from wamu import Fahrenheit, Inch, InchesMercury, InchesPerHour, MilesPerHour

from ..database import CurrentConditions
from . import BaseStation, WeatherProvider

logger = logging.getLogger(__name__)

API_ENDPOINT = "https://rt.ambientweather.net/v1"


# https://github.com/ambient-weather/api-docs/wiki/Device-Data-Specs
class API_DeviceData(BaseModel):
    dateutc: int
    date: datetime

    winddir: float | None = None
    windspeedmph: float | None = None
    windgustmph: float | None = None
    windgustdir: float | None = None

    maxdailygust: float | None = None

    winddir_avg2m: float | None = None
    windspdmph_avg2m: float | None = None

    winddir_avg10m: float | None = None
    windspdmph_avg10m: float | None = None

    tempf: float | None = None
    feelsLike: float | None = None
    dewPoint: float | None = None
    humidity: float | None = None

    baromrelin: float | None = None
    baromabsin: float | None = None

    hourlyrainin: float | None = None
    dailyrainin: float | None = None
    weeklyrainin: float | None = None
    monthlyrainin: float | None = None
    yearlyrainin: float | None = None
    eventrainin: float | None = None
    totalrainin: float | None = None

    uv: float | None = None

    tempinf: float | None = None
    humidityin: float | None = None
    feelsLikein: float | None = None
    dewPointin: float | None = None

    solarradiation: float | None = None


API_DeviceDataList = TypeAdapter(list[API_DeviceData])


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
    def observe(self) -> CurrentConditions:
        conditions = self._api_get_current_weather()

        if conditions is None:
            return None

        # read fields using correct units
        temperature = Fahrenheit(conditions.tempf)
        feels_like = Fahrenheit(conditions.feelsLike)
        dew_point = Fahrenheit(conditions.dewPoint)
        wind_speed = MilesPerHour(conditions.windspeedmph)
        wind_gust = MilesPerHour(conditions.windgustmph)
        precip_rate = InchesPerHour(conditions.hourlyrainin)
        precip_day = Inch(conditions.dailyrainin)
        precip_week = Inch(conditions.weeklyrainin)
        precip_month = Inch(conditions.monthlyrainin)
        precip_year = Inch(conditions.yearlyrainin)
        precip_total = Inch(conditions.totalrainin)
        rel_pressure = InchesMercury(conditions.baromrelin)
        abs_pressure = InchesMercury(conditions.baromabsin)

        return CurrentConditions(
            timestamp=conditions.date,
            provider=self.provider,
            station_id=self.device_id,
            temperature=temperature.fahrenheit,
            feels_like=feels_like.fahrenheit,
            dew_point=dew_point.fahrenheit,
            wind_speed=wind_speed.miles_per_hr,
            wind_gusts=wind_gust.miles_per_hr,
            wind_bearing=conditions.winddir,
            humidity=conditions.humidity,
            precip_hour=precip_rate.inches_per_hour,
            precip_day=precip_day.inches,
            precip_week=precip_week.inches,
            precip_month=precip_month.inches,
            precip_year=precip_year.inches,
            precip_total=precip_total.inches,
            rel_pressure=rel_pressure.inches_mercury,
            abs_pressure=abs_pressure.inches_mercury,
            solar_rad=conditions.solarradiation,
            uv_index=conditions.uv,
        )

    def _api_get_current_weather(self) -> API_DeviceData:
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

        data_list = API_DeviceDataList.validate_python(data)

        return data_list[0] if len(data_list) > 0 else None
