"""Application configuration data."""

import logging
import os
import os.path
from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, validator

from .providers import (
    WeatherProvider,
    accuweather,
    ambientwx,
    noaa,
    openweather,
    wunderground,
)

logger = logging.getLogger(__name__)


class Units(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"


class StationConfig(BaseModel):
    """Base configuration for weather providers."""

    __providers__ = {}

    name: str
    provider: WeatherProvider
    update_interval: Optional[int] = None

    # used techniques from https://github.com/jheddings/notional/
    def __init_subclass__(cls, provider=None, **kwargs):
        """Register the subtypes of the StationConfig class."""
        super().__init_subclass__(**kwargs)

        if provider is None:
            provider = cls.__name__

        cls._register_provider_type(provider)

    @classmethod
    def __get_validators__(cls):
        yield cls._resolve_provider_type

    @classmethod
    def _register_provider_type(cls, provider):
        """Register a specific class for the given 'provider' name."""

        if provider in cls.__providers__:
            raise ValueError(f"Duplicate subtype for class - {provider} :: {cls}")

        field = cls.__fields__.get("provider")
        field.default = provider

        logger.debug("registered new provider: %s => %s", provider, cls)

        cls.__providers__[provider] = cls

    @classmethod
    def _resolve_provider_type(cls, data):
        if isinstance(data, cls):
            return data

        if not isinstance(data, dict):
            raise ValueError("Invalid 'data' object")

        name = data.get("provider")

        if name is None:
            raise ValueError("Missing 'provider' in data")

        sub = cls.__providers__.get(name)

        if sub is None:
            raise TypeError(f"Unsupported provider: {name}")

        logger.debug("initializing provider %s :: %s => %s -- %s", cls, name, sub, data)

        return sub(**data)

    @abstractmethod
    def initialize(self):
        """Initialize a new instance of the station based on this config."""


class AmbientWeatherConfig(StationConfig, provider=WeatherProvider.AMBIENT):
    """Station configuration for Ambient Weather Network."""

    app_key: str
    user_key: str
    device_id: str

    def initialize(self):
        """Initialize a new Ambient Weather station based on this config."""

        return ambientwx.Station(
            name=self.name,
            app_key=self.app_key,
            user_key=self.user_key,
            device_id=self.device_id,
        )


class OpenWeatherMapConfig(StationConfig, provider=WeatherProvider.OPENWEATHERMAP):
    """Station configuration for OpenWeatherMap."""

    api_key: str
    latitude: float
    longitude: float

    def initialize(self):
        """Initialize a new OpenWeatherMap station based on this config."""

        return openweather.Station(
            name=self.name,
            api_key=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
        )


class WeatherUndergroundConfig(StationConfig, provider=WeatherProvider.WUNDERGROUND):
    """Station configuration for Weather Underground."""

    api_key: str
    station_id: str

    def initialize(self):
        """Initialize a new Weather Underground PWS based on this config."""

        return wunderground.Station(
            name=self.name,
            api_key=self.api_key,
            station_id=self.station_id,
        )


class AccuWeatherConfig(StationConfig, provider=WeatherProvider.ACCUWEATHER):
    """Station configuration for AccuWeather."""

    api_key: str
    location: str

    def initialize(self):
        """Initialize a new AccuWeather station based on this config."""

        return accuweather.Station(
            name=self.name,
            api_key=self.api_key,
            location=self.location,
        )


class NOAA_Config(StationConfig, provider=WeatherProvider.NOAA):
    """Station configuration for NOAA weather."""

    station: str

    def initialize(self):
        """Initialize a new NOAA station based on this config."""

        return noaa.Station(
            name=self.name,
            station=self.station,
        )


class AppConfig(BaseModel):
    """Application configuration for wxdat."""

    database: str = "sqlite:///wxdat.db"
    update_interval: int = 300
    stations: List[StationConfig] = []
    units: Units = Units.METRIC
    logging: Optional[Dict] = None
    metrics: Optional[int] = None

    @validator("database", pre=True, always=True)
    def _check_env_for_database_str(cls, val):
        env = os.getenv("WXDAT_DATABASE_URL", None)
        return val if env is None else env

    @property
    def DATABASE_CONN_STRING(self):
        return self.database

    @classmethod
    def load(cls, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"config file does not exist: {config_file}")

        with open(config_file, "r") as fp:
            data = yaml.load(fp, Loader=yaml.SafeLoader)
            conf = AppConfig(**data)

        logger = cls._configure_logging(conf)
        logger.info("loaded AppConfig from: %s", config_file)

        return conf

    @classmethod
    def _configure_logging(cls, conf):
        import logging.config

        if conf.logging is None:
            # using dictConfig() here replaces the existing configuration of all loggers
            # this approach is more predictable than logging.basicConfig(level=logging.WARN)
            logconf = {"version": 1, "incremental": False, "root": {"level": "WARN"}}

        else:
            logconf = conf.logging

        logging.config.dictConfig(logconf)

        return logging.getLogger()
