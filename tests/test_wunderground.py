"""Unit tests for the Weather Underground provider."""

import os

import pytest

from wxdat.providers import wunderground


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_query_parameters": ["apiKey"],
    }


@pytest.fixture(scope="module")
def station():
    """Return a configured Weather Underground station."""

    api_key = os.getenv("WUNDERGROUND_API_KEY", None)
    station_id = os.getenv("WUNDERGROUND_STATION", "KCODENVE549")

    if api_key is None:
        pytest.skip("missing WUNDERGROUND_API_KEY")

    yield wunderground.Station(
        "Weather Underground Test Station",
        api_key=api_key,
        station_id=station_id,
    )


@pytest.mark.vcr()
def test_wunderground_bad_api_key():
    """Verify bad Weather Underground key returns properly.""" ""

    station = wunderground.Station(
        "Invalid Key",
        api_key="bvcxz",
        station_id="KCODENVE549",
    )

    assert station.current_conditions is None


@pytest.mark.vcr()
def test_wunderground_conditions(station: wunderground.Station):
    """Test current conditions from Weather Underground."""

    conditions = station.current_conditions

    assert conditions is not None
    assert conditions.timestamp is not None
