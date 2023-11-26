"""Base funcionality for weather providers."""

import logging
from abc import ABC, abstractproperty
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import ConnectionError
from wamu.distance import Distance
from wamu.pressure import Pressure
from wamu.rate import Rate
from wamu.temperature import Temperature
from wamu.velocity import Velocity

from ..database import CurrentConditions
from ..metrics import BaseStationMetrics
from ..version import __pkgname__, __version__

logger = logging.getLogger(__name__)


class WeatherProvider(str, Enum):
    ACCUWEATHER = "AccuWeather"
    AMBIENT = "AmbientWeather"
    NOAA = "NOAA"
    OPENWEATHERMAP = "OpenWeatherMap"
    WUNDERGROUND = "WUndergroundPWS"


class Precipitation(str, Enum):
    RAIN = "rain"
    SNOW = "snow"
    ICE = "ice"
    MIXED = "mixed"


@dataclass
class WeatherObservation:
    """Current weather observations from a Station."""

    timestamp: datetime
    station: "BaseStation"

    temperature: Optional[Temperature] = None
    feels_like: Optional[Temperature] = None
    dew_point: Optional[Temperature] = None

    abs_pressure: Optional[Pressure] = None
    rel_pressure: Optional[Pressure] = None

    wind_speed: Optional[Velocity] = None
    wind_gust: Optional[Velocity] = None
    wind_bearing: Optional[float] = None

    precip_rate: Optional[Rate] = None
    precip_type: Optional[Precipitation] = None
    precip_total: Optional[Distance] = None

    cloud_cover: Optional[float] = None
    cloud_ceiling: Optional[Distance] = None
    cloud_base: Optional[Distance] = None

    humidity: Optional[float] = None
    uv_index: Optional[float] = None
    visibility: Optional[Distance] = None

    remarks: Optional[str] = None


class BaseStation(ABC):
    def __init__(self, name):
        self.name = name

        self.metrics = BaseStationMetrics(self)

        self.logger = logger.getChild("WeatherStation")
        self.logger.debug("new station: %s", name)

    @abstractproperty
    def observe(self) -> CurrentConditions:
        """Return the current conditions for this WeatherStation."""

    @abstractproperty
    def provider(self) -> WeatherProvider:
        """Return the provider name for this WeatherStation."""

    @property
    def user_agent(self):
        """Return the User-Agent string for this WeatherStation."""
        return f"{__pkgname__}/{__version__} (+https://github.com/jheddings/wxdat)"

    @sleep_and_retry
    @limits(calls=1, period=1)
    def safer_get(self, url, params=None, headers=None):
        """Convenience method to retrive a URL safely with a one second rate limit."""

        self.logger.debug("GET => %s", url)

        resp = None

        full_headers = {"User-Agent": self.user_agent}

        if headers is not None:
            full_headers.update(headers)

        try:
            resp = requests.get(url, params=params, headers=full_headers)
            self.logger.debug("=> HTTP %d: %s", resp.status_code, resp.reason)
            self.metrics.requests.inc()

        except ConnectionError:
            self.logger.warning("Unable to download data; connection error")
            self.metrics.errors.inc()
            return None

        except Exception:
            self.logger.exception("Unable to download data; unhandled exception")
            self.metrics.errors.inc()
            return None

        if not resp.ok:
            self.logger.warning("Unable to download data; HTTP %d", resp.status_code)
            self.metrics.errors.inc()
            return None

        return resp
