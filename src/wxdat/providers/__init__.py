import logging
from abc import ABC, abstractproperty
from datetime import timedelta

import requests

from ..version import __pkgname__, __version__

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

    @abstractproperty
    def provider_name(self):
        """Return the provider name for this WeatherStation."""

    @property
    def user_agent(self):
        """Return the User-Agent string for this WeatherStation."""
        return f"{__pkgname__}/{__version__} (+https://github.com/jheddings/wxdat)"

    def safe_get(self, url, params=None, headers=None):
        # XXX may want to disable this since API keys are often in the URL...
        self.logger.debug("download %s", url)

        resp = None

        full_headers = { "User-Agent": self.user_agent }

        if headers is not None:
            full_headers.update(headers)

        try:
            resp = requests.get(url, params=params, headers=full_headers)
            self.logger.debug("=> HTTP %d: %s", resp.status_code, resp.reason)

        # TODO watch for specific exceptions...
        except Exception as err:
            self.logger.error("Error downloading data: %s", exc_info=err)
            return None

        if resp is None:
            self.logger.warning("Unable to download data; empty response")
            return None
            
        if not resp.ok:
            self.logger.warning(f"Unable to download data; {resp.status_code}")
            return None

        return resp
