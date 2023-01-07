import logging
import sys
from abc import ABC, abstractproperty
from datetime import datetime, timedelta

import requests

logger = logging.getLogger(__name__)


class WeatherStation(ABC):
    def __init__(self, name):
        self.logger = logger.getChild("WeatherStation")
        self.logger.debug("new station: %s", name)

        self.name = name

        self.last_update = None
        self.update_interval = timedelta(minutes=30)

    @property
    def Name(self) -> str:
        return self.name

    @abstractproperty
    def CurrentConditions(self):
        """Return the current conditions for this WeatherStation."""

    @property
    def is_current(self):
        if self.last_update is None:
            return False

        now = datetime.now()
        delta = now - self.last_update

        self.logger.debug(
            "station %s last updated at %s (%s ago)", self.name, self.last_update, delta
        )

        return delta <= self.update_interval

    def safe_get(self, url, params=None):
        # XXX may want to disable this since API keys are often in the URL...
        self.logger.debug("download %s", url)

        resp = None

        try:
            resp = requests.get(url, params)
            self.logger.debug("=> HTTP %d: %s", resp.status_code, resp.reason)

            # TODO watch for specific exceptions...
        except Exception:
            self.logger.error("Error downloading data: %s", sys.exc_info()[0])
            resp = None

        if resp is None or not resp.ok:
            self.logger.warning("Could not download data")

        return resp
