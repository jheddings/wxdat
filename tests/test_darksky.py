"""Unit tests for the Dark Sky provider."""

import pytest

from wxdat.providers import darksky


@pytest.mark.vcr()
def test_bad_api_key():
    station = darksky.Station(
        "Invalid Key", api_key="xyz123", latitude=39.73465, longitude=-104.98672
    )

    assert station.current_conditions is None
