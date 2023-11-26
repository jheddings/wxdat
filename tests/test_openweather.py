"""Unit tests for the OpenWeatherMap provider."""

import os

import pytest

from wxdat.providers import openweather


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_query_parameters": ["appid"],
    }


@pytest.fixture(scope="function")
def station():
    """Return a configured Ambient Weather station."""

    api_key = os.getenv("OPENWEATHER_API_KEY", None)

    if api_key is None:
        pytest.skip("missing OPENWEATHER_API_KEY")

    yield openweather.Station(
        "OpenWeatherMap Test Station",
        api_key=api_key,
        latitude=39.73465,
        longitude=-104.98672,
    )


@pytest.mark.vcr()
def test_openweather_bad_api_key():
    """Verify bad OpenWeatherMap key returns properly."""

    station = openweather.Station(
        "Invalid Key",
        api_key="qwerty",
        latitude=39.73465,
        longitude=-104.98672,
    )

    assert station.observe is None


@pytest.mark.vcr()
def test_openweather_conditions(station: openweather.Station):
    """Test current conditions from OpenWeatherMap."""

    conditions = station.observe

    assert conditions is not None
    assert conditions.timestamp is not None
