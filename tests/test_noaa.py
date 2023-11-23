"""Unit tests for the NOAA provider."""

import pytest

from wxdat.providers import noaa


@pytest.fixture(scope="module", params=["KDEN", "KSEA"])
def station(request):
    """Return a configured NOAA station."""

    yield noaa.Station("NOAA Test Station", station=request.param)


@pytest.mark.vcr()
def test_bad_station():
    """Verify bad NOAA station returns properly."""

    station = noaa.Station("Bad Station", station="XXXX")

    assert station.current_conditions is None


@pytest.mark.vcr()
def test_noaa_conditions(station: noaa.Station):
    """Test current conditions from NOAA."""

    conditions = station.current_conditions

    assert conditions is not None
    assert conditions.timestamp is not None

    # some basic checks on the contents
    assert type(conditions.temperature) in [int, float]
    assert type(conditions.humidity) in [int, float]
    assert type(conditions.wind_speed) in [int, float]
