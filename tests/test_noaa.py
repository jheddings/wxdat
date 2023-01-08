"""Unit tests for the NOAA provider."""

import pytest

from wxdat.providers import noaa


@pytest.mark.vcr()
def test_bad_station():
    station = noaa.Station("Bad Station", station="XXXX")

    wx = station.get_current_weather()

    assert wx is None
