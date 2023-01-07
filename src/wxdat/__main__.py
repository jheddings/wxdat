"""Main entry point for wxdat."""

import logging
import signal
import threading

import click

from .config import AppConfig
from .providers import DataRecorder

logger = logging.getLogger(__name__)


class MainApp:
    """Context used during main execution."""

    def __init__(self, config: AppConfig):
        self.logger = logger.getChild("MainApp")

        self.config = config
        self.run_lock = threading.Event()

        self._initialize_database(config.database)
        self._initialize_observers(config)

    def _initialize_observers(self, config: AppConfig):
        self.observers = []

        for station_cfg in config.stations:
            station = station_cfg.initialize()
            interval = station_cfg.update_interval or config.update_interval
            recorder = DataRecorder(station, self.database, interval)
            self.observers.append(recorder)

    def _initialize_database(self, dburl):
        from .database import WeatherDatabase

        self.database = WeatherDatabase(dburl)

    def run(self):

        self.logger.debug("Starting main app")

        for obs in self.observers:
            obs.start()

        try:
            signal.pause()
        except KeyboardInterrupt:
            self.logger.debug("canceled by user")

        for obs in self.observers:
            obs.stop()


@click.command()
@click.option(
    "--config", "-f", default="wxdat.yaml", help="app config file (default: wxdat.yaml)"
)
def main(config):
    cfg = AppConfig.load(config)

    MainApp(cfg).run()


### MAIN ENTRY
if __name__ == "__main__":
    main()
