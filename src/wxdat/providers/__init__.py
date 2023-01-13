"""Base funcionality for weather providers."""

import logging
import threading
from abc import ABC, abstractproperty
from datetime import datetime, timedelta
from enum import Enum

import requests
from ratelimit import limits, sleep_and_retry
from requests.exceptions import ConnectionError

from ..database import CurrentConditions, WeatherDatabase
from ..version import __pkgname__, __version__

logger = logging.getLogger(__name__)


class WeatherProvider(str, Enum):
    ACCUWEATHER = "AccuWeather"
    AMBIENT = "AmbientWeather"
    DARKSKY = "DarkSky"
    NOAA = "NOAA"
    OPENWEATHERMAP = "OpenWeatherMap"
    WUNDERGROUND = "WUndergroundPWS"


class BaseStation(ABC):
    def __init__(self, name):
        self.name = name

        self.logger = logger.getChild("WeatherStation")
        self.logger.debug("new station: %s", name)

    @abstractproperty
    def current_conditions(self) -> CurrentConditions:
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

        except ConnectionError:
            self.logger.warning("Unable to download data; connection error")
            return None

        except Exception:
            self.logger.exception("Unable to download data; unhandled exception")
            return None

        if not resp.ok:
            self.logger.warning("Unable to download data; %d", resp.status_code)
            return None

        return resp


class DataRecorder:
    """Records data from a specific BaseStation."""

    __thread_count__ = 0

    def __init__(self, station: BaseStation, database: WeatherDatabase, interval):
        DataRecorder.__thread_count__ += 1

        self.station = station
        self.database = database
        self.interval = interval

        self.thread_ctl = threading.Event()
        self.loop_thread = threading.Thread(name=self.id, target=self.run_loop)
        self.loop_last_exec = None

        self.logger = logger.getChild("DataRecorder")

    @property
    def id(self) -> str:
        return f"{self.station.provider}-{DataRecorder.__thread_count__}"

    def start(self) -> None:
        """Start the main thread loop."""

        self.logger.debug("Starting WeatherApp thread")

        self.thread_ctl.clear()
        self.loop_thread.start()

    def stop(self) -> None:
        """Signal the thread to stop and wait for it to exit."""

        self.logger.debug("Stopping WeatherApp thread")

        self.thread_ctl.set()
        self.loop_thread.join(self.interval)

        if self.loop_thread.is_alive():
            self.logger.warning("Thread failed to complete")

    def run_loop(self):
        """Manage the lifecycle of the thread loop."""

        self.logger.debug(
            "BEGIN -- %s :: run_loop @ %f sec", self.station.name, self.interval
        )

        while not self.thread_ctl.is_set():
            self.loop_last_exec = datetime.now()

            self.record_current_conditions()

            # figure out when to run the next step
            elapsed = (datetime.now() - self.loop_last_exec).total_seconds()
            next_loop_time = self.loop_last_exec + timedelta(seconds=self.interval)
            next_loop_sleep = (next_loop_time - datetime.now()).total_seconds()

            if next_loop_sleep <= 0:
                self.logger.warning("loop time exceeded interval; overflow")
                next_loop_sleep = 0

            self.logger.debug(
                "%s :: run_loop complete; %f sec elapsed (next_step: %f)",
                self.station.name,
                elapsed,
                next_loop_sleep,
            )

            # break if we are signaled to stop
            if self.thread_ctl.wait(next_loop_sleep):
                self.logger.debug("received exit signal; run_loop exiting")

        self.logger.debug("END -- %s :: run_loop", self.station.name)

    def record_current_conditions(self):
        """Record the current conditions from the internal station."""

        self.logger.info("Updating station data -- %s", self.station.name)
        wx_data = self.station.current_conditions

        if wx_data is None:
            self.logger.warning("Unable to get current conditions")
            return False

        self.logger.debug("-- saving current data @ %s", wx_data.timestamp)
        return self.database.save(wx_data)
