"""Base funcionality for weather providers."""

import logging
from abc import ABC, abstractproperty
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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

    temperature: Temperature | None = None
    feels_like: Temperature | None = None
    dew_point: Temperature | None = None

    abs_pressure: Pressure | None = None
    rel_pressure: Pressure | None = None

    wind_speed: Velocity | None = None
    wind_gust: Velocity | None = None
    wind_bearing: float | None = None

    precip_rate: Rate | None = None
    precip_type: Precipitation | None = None
    precip_total: Distance | None = None

    cloud_cover: float | None = None
    cloud_ceiling: Distance | None = None
    cloud_base: Distance | None = None

    humidity: float | None = None
    uv_index: float | None = None
    visibility: Distance | None = None

    remarks: str | None = None


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
