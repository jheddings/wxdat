"""Unit tests for the Ambient Weather provider."""

import pytest

from wxdat.providers import ambientwx


@pytest.mark.vcr()
def test_bad_api_key():
    station = ambientwx.Station(
        "Invalid Key",
        app_key="xyz123",
        user_key="456pqd",
        device_id="eb:8d:60:8a:33:e7",
    )

    assert station.current_conditions is None
