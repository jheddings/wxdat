"""Application configuration data."""

import os
import os.path
from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, validator
from ruamel.yaml import YAML

from .providers import (
    WeatherProvider,
    accuweather,
    ambientwx,
    darksky,
    noaa,
    openweather,
    wunderground,
)


class Units(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"


class StationConfig(BaseModel):
    """Base configuration for weather providers."""

    name: str
    provider: WeatherProvider
    update_interval: Optional[int] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.resolve_provider_type

    @classmethod
    def resolve_provider_type(cls, data):
        if "provider" not in data:
            raise ValueError("missing 'provider' in station config")

        if data["provider"] == WeatherProvider.AMBIENT:
            return AmbientWeatherConfig(**data)

        if data["provider"] == WeatherProvider.WUNDERGROUND:
            return WeatherUndergroundConfig(**data)

        if data["provider"] == WeatherProvider.OPENWEATHER:
            return OpenWeatherMapConfig(**data)

        if data["provider"] == WeatherProvider.DARKSKY:
            return DarkSkyConfig(**data)

        if data["provider"] == WeatherProvider.ACCUWEATHER:
            return AccuWeatherConfig(**data)

        if data["provider"] == WeatherProvider.NOAA:
            return NOAA_Config(**data)

        raise ValueError(f"unsupported provider -- {data['provider']}")

    @abstractmethod
    def initialize(self):
        """Initialize a new instance of the station based on this config."""


class AmbientWeatherConfig(StationConfig):
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


class OpenWeatherMapConfig(StationConfig):
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


class DarkSkyConfig(StationConfig):
    """Station configuration for Dark Sky."""

    api_key: str
    latitude: float
    longitude: float

    def initialize(self):
        """Initialize a new Dark Sky station based on this config."""

        return darksky.Station(
            name=self.name,
            api_key=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
        )


class WeatherUndergroundConfig(StationConfig):
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


class AccuWeatherConfig(StationConfig):
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


class NOAA_Config(StationConfig):
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

        yaml = YAML(typ="safe")

        with open(config_file, "r") as fp:
            data = yaml.load(fp)
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
