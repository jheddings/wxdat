"""Unit tests for the OpenWeatherMap provider."""

import pytest

from wxdat.providers import openweather


@pytest.mark.vcr()
def test_bad_api_key():
    station = openweather.Station(
        "Invalid Key", api_key="qwerty", latitude=39.73465, longitude=-104.98672
    )

    assert station.current_conditions is None
