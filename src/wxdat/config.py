"""Application configuration data."""

import os
import os.path
from abc import abstractmethod
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, validator
from ruamel.yaml import YAML

from .stations import ambientwx, openweather


class Units(str, Enum):
    IMPERIAL = "imperial"
    METRIC = "metric"


class WeatherProvider(str, Enum):
    AMBIENT = "AmbientWeather"
    DARKSKY = "DarkSky"
    OPENWEATHER = "OpenWeatherMap"
    WUNDERGROUND = "WUndergroundPWS"


class ProviderConfig(BaseModel):
    """Base configuration for weather providers."""

    name: str
    type: WeatherProvider

    # TODO support per-station update intervals
    update_interval: Optional[int] = None

    @classmethod
    def __get_validators__(cls):
        yield cls.resolve_provider_type

    @classmethod
    def resolve_provider_type(cls, data):
        if "type" not in data:
            raise ValueError("missing 'type' in provider config")

        if data["type"] == WeatherProvider.AMBIENT:
            return AmbientWeatherConfig(**data)

        if data["type"] == WeatherProvider.WUNDERGROUND:
            return WeatherUndergroundConfig(**data)

        if data["type"] == WeatherProvider.OPENWEATHER:
            return OpenWeatherMapConfig(**data)

        if data["type"] == WeatherProvider.DARKSKY:
            return DarkSkyConfig(**data)

        raise ValueError(f"unsupported provider -- {data['type']}")

    @abstractmethod
    def initialize(self):
        """Initialize a new instance of the station based on this config."""


class AmbientWeatherConfig(ProviderConfig):
    """Provider configuration for Ambient Weather Network."""

    app_key: str
    user_key: str
    device_id: str

    def initialize(self):
        """Initialize a new Ambient Weather station based on this config."""
        return ambientwx.AmbientWeather(
            name=self.name,
            app_key=self.app_key,
            user_key=self.user_key,
            device_id=self.device_id,
        )


class OpenWeatherMapConfig(ProviderConfig):
    """Provider configuration for OpenWeatherMap."""

    api_key: str
    latitude: float
    longitude: float

    def initialize(self):
        """Initialize a new OpenWeatherMap station based on this config."""
        return openweather.OpenWeatherMap(
            name=self.name,
            api_key=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
        )


class DarkSkyConfig(ProviderConfig):
    """Provider configuration for Dark Sky."""

    api_key: str
    latitude: float
    longitude: float

    def initialize(self):
        """Initialize a new Dark Sky station based on this config."""


class WeatherUndergroundConfig(ProviderConfig):
    """Provider configuration for Weather Underground."""

    api_key: str
    station_id: str

    def initialize(self):
        """Initialize a new Weather Underground PWS based on this config."""


class AppConfig(BaseModel):
    """Application configuration for wxdat."""

    database: str = "sqlite:///wxdat.db"
    update_interval: int = 300
    stations: List[ProviderConfig] = []
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
