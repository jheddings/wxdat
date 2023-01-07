"""Main entry point for wxdat."""


import logging
import signal
import threading

import click

from .config import AppConfig

logger = logging.getLogger(__name__)


class MainApp:
    """Context used during main execution."""

    def __init__(self, config: AppConfig):
        self.logger = logger.getChild("MainApp")

        self.config = config
        self.run_lock = threading.Event()

        self._initialize_database(config.database)
        self._initialize_observer(config)

    def _initialize_observer(self, config: AppConfig):
        from . import Observer

        observer = Observer(self.database, config.update_interval)

        for station_cfg in config.stations:
            station = station_cfg.initialize()
            observer.watch(station)

        self.observer = observer

    def _initialize_database(self, dburl):
        from .database import WeatherDatabase

        self.database = WeatherDatabase(dburl)

    def run(self):

        self.logger.debug("Starting main app")

        self.observer.start()

        try:
            signal.pause()
        except KeyboardInterrupt:
            self.logger.debug("canceled by user")

        self.observer.stop()


@click.command()
@click.option(
    "--config", "-f", default="wxdat.yaml", help="app config file (default: wxdat.yaml)"
)
def main(config):
    conf = AppConfig.load(config)

    app = MainApp(conf)

    app.run()


### MAIN ENTRY
if __name__ == "__main__":
    main()
