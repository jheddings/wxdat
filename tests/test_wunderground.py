"""Unit tests for the Weather Underground provider."""

import pytest

from wxdat.providers import wunderground


@pytest.mark.vcr()
def test_bad_api_key():
    station = wunderground.Station(
        "Invalid Key", api_key="bvcxz", station_id="KCODENVE549"
    )

    assert station.current_conditions is None
