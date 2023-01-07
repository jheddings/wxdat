import logging
import sys
from abc import ABC, abstractproperty
from datetime import timedelta

import requests

logger = logging.getLogger(__name__)


class WeatherStation(ABC):
    def __init__(self, name):
        self.logger = logger.getChild("WeatherStation")
        self.logger.debug("new station: %s", name)

        self.name = name

        # TODO add support for station-specific update intervals
        self.update_interval = timedelta(minutes=30)

    @abstractproperty
    def current_conditions(self):
        """Return the current conditions for this WeatherStation."""

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
