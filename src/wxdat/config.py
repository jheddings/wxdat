"""Application configuration data."""

import logging
import os
import os.path
from abc import abstractmethod
from enum import Enum
from typing import Annotated, Dict, List, Literal, Optional, Union

import yaml
from pydantic import BaseModel, Field, validator

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


class StationConfigBase(BaseModel):
    """Base configuration for weather providers."""

    __providers__ = {}

    name: str
    provider: WeatherProvider
    update_interval: Optional[int] = None

    @abstractmethod
    def initialize(self):
        """Initialize a new instance of the station based on this config."""


class AccuWeatherConfig(StationConfigBase):
    """Station configuration for AccuWeather."""

    api_key: str
    location: Union[str, int]
    provider: Literal[WeatherProvider.ACCUWEATHER]

    def initialize(self):
        """Initialize a new AccuWeather station based on this config."""

        return accuweather.Station(
            name=self.name,
            api_key=self.api_key,
            location=self.location,
        )


class AmbientWeatherConfig(StationConfigBase):
    """Station configuration for Ambient Weather Network."""

    app_key: str
    user_key: str
    device_id: str
    provider: Literal[WeatherProvider.AMBIENT]

    def initialize(self):
        """Initialize a new Ambient Weather station based on this config."""

        return ambientwx.Station(
            name=self.name,
            app_key=self.app_key,
            user_key=self.user_key,
            device_id=self.device_id,
        )


class NOAA_Config(StationConfigBase):
    """Station configuration for NOAA weather."""

    station: str
    provider: Literal[WeatherProvider.NOAA]

    def initialize(self):
        """Initialize a new NOAA station based on this config."""

        return noaa.Station(
            name=self.name,
            station=self.station,
        )


class OpenWeatherMapConfig(StationConfigBase):
    """Station configuration for OpenWeatherMap."""

    api_key: str
    latitude: float
    longitude: float
    provider: Literal[WeatherProvider.OPENWEATHERMAP]

    def initialize(self):
        """Initialize a new OpenWeatherMap station based on this config."""

        return openweather.Station(
            name=self.name,
            api_key=self.api_key,
            latitude=self.latitude,
            longitude=self.longitude,
        )


class WeatherUndergroundConfig(StationConfigBase):
    """Station configuration for Weather Underground."""

    api_key: str
    station_id: str
    provider: Literal[WeatherProvider.WUNDERGROUND]

    def initialize(self):
        """Initialize a new Weather Underground PWS based on this config."""

        return wunderground.Station(
            name=self.name,
            api_key=self.api_key,
            station_id=self.station_id,
        )


StationConfig = Annotated[
    Union[
        AccuWeatherConfig,
        AmbientWeatherConfig,
        NOAA_Config,
        OpenWeatherMapConfig,
        WeatherUndergroundConfig,
    ],
    Field(discriminator="provider"),
]


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

    @classmethod
    def load(cls, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"config file does not exist: {config_file}")

        with open(config_file) as fp:
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
