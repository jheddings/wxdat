"""Unit tests for the NOAA provider."""

import pytest

from wxdat.providers import noaa


@pytest.mark.vcr()
def test_bad_station():
    station = noaa.Station("Bad Station", station="XXXX")

    assert station.current_conditions is None
