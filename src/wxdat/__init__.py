"""Module interface to wxdat."""

import logging
import threading
from datetime import datetime, timedelta

from .database import WeatherDatabase
from .stations import WeatherStation

logger = logging.getLogger(__name__)


class Observer:
    """Oberves and records weather data on a defined interval."""

    def __init__(self, database: WeatherDatabase, interval=300):
        """Initialize the observer."""

        self.database = database
        self.update_interval = interval

        self.stations = []
        self.stations_lock = threading.Lock()

        self.thread_ctl = threading.Event()
        self.loop_thread = threading.Thread(target=self.run_loop)
        self.loop_last_exec = None

        self.logger = logger.getChild("Observer")

    def watch(self, station) -> None:
        """Watch the provided station."""

        if station is None:
            raise ValueError("station cannot be None")

        with self.stations_lock:
            self.stations.append(station)

    def start(self) -> None:
        """Start the main thread loop."""

        self.logger.debug("Starting WeatherApp thread")

        self.thread_ctl.clear()
        self.loop_thread.start()

    def stop(self) -> None:
        """Signal the thread to stop and wait for it to exit."""

        self.logger.debug("Stopping WeatherApp thread")

        self.thread_ctl.set()
        self.loop_thread.join(self.update_interval)

        if self.loop_thread.is_alive():
            self.logger.warning("Thread failed to complete")

    def run_loop(self):
        """Manage the lifecycle of the thread loop."""

        self.logger.debug(
            "BEGIN -- WeatherApp::run_loop @ %f sec", self.update_interval
        )

        while not self.thread_ctl.is_set():

            self.loop_last_exec = datetime.now()

            self.thread_loop_step()

            # figure out when to run the next step
            next_loop_time = self.loop_last_exec + timedelta(
                seconds=self.update_interval
            )
            next_loop_sleep = (next_loop_time - datetime.now()).total_seconds()

            if next_loop_sleep <= 0:
                self.logger.warning(
                    "WeatherApp :: thread_loop_step time exceeded interval; overflow"
                )
                next_loop_sleep = 0

            # break if we are signaled to stop
            if self.thread_ctl.wait(next_loop_sleep):
                self.logger.debug("received exit signal; ThreadLoop exiting")

        self.logger.debug("END -- WeatherApp::run_loop")

    def thread_loop_step(self):
        """Performs the main work for the thread loop."""

        with self.stations_lock:
            for station in self.stations:
                self.update_station_data(station)

    def update_station_data(self, station: WeatherStation):
        self.logger.info("Updating station data -- %s", station.name)
        wx_data = station.current_conditions

        self.logger.debug("-- saving current data @ %s", wx_data.timestamp)
        self.database.save(wx_data)
