"""Unit tests for the AccuWeather provider."""

import os

import pytest

from wxdat.providers import accuweather


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_query_parameters": ["apikey"],
    }


@pytest.fixture(scope="module")
def station():
    """Return a configured AccuWeather station."""

    api_key = os.getenv("ACCUWEATHER_API_KEY", None)
    location = os.getenv("ACCUWEATHER_LOCATION", "347810")

    if api_key is None:
        pytest.skip("missing ACCUWEATHER_API_KEY")

    yield accuweather.Station(
        "AccuWeather Test Station",
        api_key=api_key,
        location=location,
    )


@pytest.mark.vcr()
def test_accuweather_bad_api_key():
    """Verify bad AccuWeather key returns properly."""

    station = accuweather.Station("Invalid Key", api_key="12345", location=2626674)

    assert station.current_conditions is None


@pytest.mark.vcr()
def test_accuweather_conditions(station: accuweather.Station):
    """Test current conditions from AccuWeather."""

    conditions = station.current_conditions

    assert conditions is not None
    assert conditions.timestamp is not None
