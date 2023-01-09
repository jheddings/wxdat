"""Unit tests for the NOAA provider."""

import pytest

from wxdat.providers import noaa


@pytest.mark.vcr()
def test_bad_station():
    station = noaa.Station("Bad Station", station="XXXX")

    assert station.current_conditions is None


@pytest.mark.vcr()
def test_denver_station():
    station = noaa.Station("Denver Airport", station="KDEN")
    cond = station.current_conditions

    assert cond is not None
    assert cond.station_id == "KDEN"

    # some basic checks on the contents
    assert type(cond.temperature) in [int, float]
    assert type(cond.humidity) in [int, float]
    assert type(cond.wind_speed) in [int, float]
