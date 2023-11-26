"""Record weather data from a BaseStation."""

import logging
import threading
from datetime import datetime, timedelta

from .database import WeatherDatabase
from .metrics import WeatherConditionMetrics
from .providers import BaseStation

logger = logging.getLogger(__name__)


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

        self.metrics = WeatherConditionMetrics(station)

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

        self.logger.info("Reading current condition -- %s", self.station.name)
        obs = self.station.observe

        if obs is None:
            self.logger.debug(
                "Station '%s' did not provide current weather.",
                self.station.name,
            )
            return False

        self.metrics.update(obs)

        self.logger.debug("-- saving current data @ %s", obs.timestamp)

        # if we succesfully record the data, update the total readings for the station...  it's a bit
        # hacky to reach into the station this way, but this is the only place we can be sure that the
        # data has been stored in the database and have reference to the station identifiers
        if self.database.save(obs):
            self.station.metrics.readings.inc()
        else:
            self.station.metrics.failed.inc()

        return True
