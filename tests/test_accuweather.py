"""Unit tests for the AccuWeather provider."""

import pytest

from wxdat.providers import accuweather


@pytest.mark.vcr()
def test_bad_api_key():
    station = accuweather.Station("Invalid Key", api_key="12345", location=2626674)

    assert station.current_conditions is None
