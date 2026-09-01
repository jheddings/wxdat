"""Unit tests for the NOAA provider."""

import logging

import pytest

from wxdat.providers import noaa

# Expected observation values per station, verified against the raw METAR recorded in
# each cassette.  The NWS API reports wind in km/h; the METAR reports it in knots.
EXPECTED = {
    # KDEN 081653Z 22013KT 10SM CLR M04/M12 A3023 -- 13 kt sustained, no gust
    "KDEN": {
        "temperature": 24.08,
        "feels_like": 11.45,
        "dew_point": 10.94,
        "wind_speed": 14.9875,
        "wind_gusts": None,
        "wind_bearing": 220,
        "humidity": 56.7556,
        "precip_hour": None,
        "abs_pressure": None,
        "rel_pressure": 30.3686,
        "visibility": 9.9979,
    },
    # KSEA 081653Z 00000KT 10SM BKN022 06/04 A3050 -- calm
    "KSEA": {
        "temperature": 42.98,
        "feels_like": None,
        "dew_point": 39.92,
        "wind_speed": 0.0,
        "wind_gusts": None,
        "wind_bearing": 0,
        "humidity": 88.8585,
        "precip_hour": None,
        "abs_pressure": 30.5015,
        "rel_pressure": 30.5251,
        "visibility": 9.9979,
    },
}


@pytest.fixture(scope="function", params=["KDEN", "KSEA"])
def station(request):
    """Return a configured NOAA station."""

    yield noaa.Station("NOAA Test Station", station=request.param)


@pytest.mark.vcr()
def test_bad_station():
    """Verify bad NOAA station returns properly."""

    station = noaa.Station("Bad Station", station="XXXX")

    assert station.observe is None


@pytest.mark.vcr()
def test_noaa_conditions(station: noaa.Station):
    """Test current conditions from NOAA."""

    conditions = station.observe

    assert conditions is not None
    assert conditions.timestamp is not None

    for field, value in EXPECTED[station.station].items():
        observed = getattr(conditions, field)

        if value is None:
            assert observed is None, field
        else:
            assert observed == pytest.approx(value, abs=0.0001), field


def measurement(unit_code, value):
    """Return an API measurement reported in the given unit."""

    return noaa.API_Measurement(unitCode=unit_code, qualityControl="V", value=value)


def test_convert_speed_from_kilometers_per_hour():
    """Verify a speed reported in km/h converts to mph."""

    assert noaa.convert(measurement("wmoUnit:km_h-1", 24.12), noaa.MILES_PER_HOUR) == pytest.approx(
        14.99, abs=0.01
    )


def test_convert_speed_from_meters_per_second():
    """Verify a speed reported in m/s converts to mph."""

    assert noaa.convert(measurement("wmoUnit:m_s-1", 24.12), noaa.MILES_PER_HOUR) == pytest.approx(
        53.95, abs=0.01
    )


def test_convert_unrecognized_unit_is_dropped(caplog):
    """Verify an unexpected unit is dropped with a warning instead of being assumed."""

    with caplog.at_level(logging.WARNING):
        value = noaa.convert(measurement("wmoUnit:kt", 13.0), noaa.MILES_PER_HOUR)

    assert value is None
    assert "wmoUnit:kt" in caplog.text


def test_convert_absent_measurement_is_none():
    """Verify a measurement missing from the response converts to nothing."""

    assert noaa.convert(None, noaa.MILES_PER_HOUR) is None


def test_convert_empty_measurement_is_none():
    """Verify a measurement reported without a value converts to nothing."""

    assert noaa.convert(measurement("wmoUnit:km_h-1", None), noaa.MILES_PER_HOUR) is None


def test_convert_temperature_from_celsius():
    """Verify a temperature reported in degrees C converts to degrees F."""

    assert noaa.convert(measurement("wmoUnit:degC", 100.0), noaa.FAHRENHEIT) == pytest.approx(
        212.0, abs=0.0001
    )


def test_convert_pressure_from_pascals():
    """Verify a pressure reported in pascals converts to inches of mercury."""

    assert noaa.convert(measurement("wmoUnit:Pa", 101325.0), noaa.INCHES_MERCURY) == pytest.approx(
        29.9213, abs=0.0001
    )


def test_convert_distance_from_meters():
    """Verify a distance reported in meters converts to miles."""

    assert noaa.convert(measurement("wmoUnit:m", 1609.344), noaa.MILES) == pytest.approx(
        1.0, abs=0.0001
    )


def test_convert_precipitation_from_millimeters():
    """Verify hourly precipitation reported in mm converts to inches per hour."""

    assert noaa.convert(measurement("wmoUnit:mm", 25.4), noaa.INCHES_PER_HOUR) == pytest.approx(
        1.0, abs=0.0001
    )
