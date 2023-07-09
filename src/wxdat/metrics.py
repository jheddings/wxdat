"""Metrics provider for wxdat."""

from typing import Optional

from prometheus_client import Counter, Gauge

PROVIDER_REQUESTS = Counter(
    "wxdat_provider_requests",
    "Total requests made to a provider.",
    labelnames=["station", "provider", "method"],
)

STATION_READINGS = Counter(
    "wxdat_station_readings",
    "Readings recorded by the station.",
    labelnames=["station"],
)

STATION_FAILED = Counter(
    "wxdat_station_failed",
    "Failures during station readings.",
    labelnames=["station"],
)

STATION_ERRORS = Counter(
    "wxdat_station_errors",
    "Errors reported by the station.",
    labelnames=["station"],
)

CURRENT_TEMPERATURE = Gauge(
    "wxdat_current_temperature",
    "Current temperature reported by the station.",
    labelnames=["station"],
)

CURRENT_FEELS_LIKE = Gauge(
    "wxdat_current_feels_like_temperature",
    "Current 'feels like' temperature reported by the station.",
    labelnames=["station"],
)

CURRENT_DEWPOINT = Gauge(
    "wxdat_current_dewpoint",
    "Current dewpoint reported by the station.",
    labelnames=["station"],
)

CURRENT_WIND_SPEED = Gauge(
    "wxdat_current_wind_speed",
    "Current wind speed reported by the station.",
    labelnames=["station"],
)

CURRENT_WIND_GUSTS = Gauge(
    "wxdat_current_wind_gusts",
    "Current wind gusts reported by the station.",
    labelnames=["station"],
)

CURRENT_WIND_BEARING = Gauge(
    "wxdat_current_wind_bearing",
    "Current wind bearing reported by the station.",
    labelnames=["station"],
)

TOTAL_PRECIP = Counter(
    "wxdat_precipitation",
    "Precipitation reported by the station.",
    labelnames=["station"],
)

CURRENT_HUMIDITY = Gauge(
    "wxdat_current_humidity",
    "Current humidity reported by the station.",
    labelnames=["station"],
)

CURRENT_REL_PRESSURE = Gauge(
    "wxdat_current_rel_pressure",
    "Current relative pressure reported by the station.",
    labelnames=["station"],
)

CURRENT_ABS_PRESSURE = Gauge(
    "wxdat_current_abs_pressure",
    "Current absolute pressure reported by the station.",
    labelnames=["station"],
)

CURRENT_CLOUDS = Gauge(
    "wxdat_current_clouds",
    "Current cloud cover reported by the station.",
    labelnames=["station"],
)

CURRENT_VISIBILITY = Gauge(
    "wxdat_current_visibility",
    "Current visibility reported by the station.",
    labelnames=["station"],
)

CURRENT_UV_INDEX = Gauge(
    "wxdat_current_uv_index",
    "Current UV index reported by the station.",
    labelnames=["station"],
)

CURRENT_OZONE = Gauge(
    "wxdat_current_ozone",
    "Current ozone reported by the station.",
    labelnames=["station"],
)

CURRENT_SOLAR_LUX = Gauge(
    "wxdat_current_solar_lux",
    "Current solar level reported by the station.",
    labelnames=["station"],
)

CURRENT_SOLAR_RAD = Gauge(
    "wxdat_current_solar_radiation",
    "Current solar radiation reported by the station.",
    labelnames=["station"],
)


class DatabaseMetrics:
    def __init__(self, engine):
        self._engine = engine

        self.sessions = Counter("wxdat_session_created", "Database sessions created")
        self.writes = Counter("wxdat_session_writes", "Database write attemps")
        self.commits = Counter("wxdat_session_commits", "Database commits completed")
        self.errors = Counter("wxdat_session_errors", "Database session errors")


class BaseStationMetrics:
    def __init__(self, station):
        self.readings = STATION_READINGS.labels(station=station.name)
        self.errors = STATION_ERRORS.labels(station=station.name)
        self.failed = STATION_FAILED.labels(station=station.name)

        self.requests = PROVIDER_REQUESTS.labels(
            method="get",
            provider=station.provider.value,
            station=station.name,
        )


class WeatherConditionMetrics:
    def __init__(self, station):
        name = station.name

        self.temperature = CURRENT_TEMPERATURE.labels(station=name)
        self.feels_like = CURRENT_FEELS_LIKE.labels(station=name)
        self.dew_point = CURRENT_DEWPOINT.labels(station=name)

        self.wind_speed = CURRENT_WIND_SPEED.labels(station=name)
        self.wind_gusts = CURRENT_WIND_GUSTS.labels(station=name)
        self.wind_bearing = CURRENT_WIND_BEARING.labels(station=name)

        self.precipitation = TOTAL_PRECIP.labels(station=name)
        self.humidity = CURRENT_HUMIDITY.labels(station=name)

        self.rel_pressure = CURRENT_REL_PRESSURE.labels(station=name)
        self.abs_pressure = CURRENT_ABS_PRESSURE.labels(station=name)

        self.cloud_cover = CURRENT_CLOUDS.labels(station=name)
        self.visibility = CURRENT_VISIBILITY.labels(station=name)
        self.uv_index = CURRENT_UV_INDEX.labels(station=name)
        self.ozone = CURRENT_OZONE.labels(station=name)

        self.solar_lux = CURRENT_SOLAR_LUX.labels(station=name)
        self.solar_rad = CURRENT_SOLAR_RAD.labels(station=name)

    def _update_gauge(self, gauge: Gauge, val: Optional[float] = None):
        if val is not None:
            gauge.set(val)

    def update(self, current_conditions):
        self._update_gauge(self.temperature, current_conditions.temperature)
        self._update_gauge(self.feels_like, current_conditions.feels_like)
        self._update_gauge(self.dew_point, current_conditions.dew_point)
        self._update_gauge(self.wind_speed, current_conditions.wind_speed)
        self._update_gauge(self.wind_gusts, current_conditions.wind_gusts)
        self._update_gauge(self.wind_bearing, current_conditions.wind_bearing)
        self._update_gauge(self.precipitation, current_conditions.precip_total)
        self._update_gauge(self.humidity, current_conditions.humidity)
        self._update_gauge(self.rel_pressure, current_conditions.rel_pressure)
        self._update_gauge(self.abs_pressure, current_conditions.abs_pressure)
        self._update_gauge(self.cloud_cover, current_conditions.cloud_cover)
        self._update_gauge(self.visibility, current_conditions.visibility)
        self._update_gauge(self.uv_index, current_conditions.uv_index)
        self._update_gauge(self.ozone, current_conditions.ozone)
        self._update_gauge(self.solar_lux, current_conditions.solar_lux)
        self._update_gauge(self.solar_rad, current_conditions.solar_rad)
