"""Unit tests for the Ambient Weather provider."""

import os

import pytest

from wxdat.providers import ambientwx


@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_query_parameters": ["apiKey", "applicationKey"],
    }


@pytest.fixture(scope="module")
def station():
    """Return a configured Ambient Weather station."""

    app_key = os.getenv("AMBIENT_WX_APP_KEY", None)
    user_key = os.getenv("AMBIENT_WX_USER_KEY", None)
    device_id = os.getenv("AMBIENT_WX_DEVICE_ID", None)

    if app_key is None:
        pytest.skip("missing AMBIENT_WX_APP_KEY")

    if user_key is None:
        pytest.skip("missing AMBIENT_WX_USER_KEY")

    if device_id is None:
        pytest.skip("missing AMBIENT_WX_DEVICE_ID")

    yield ambientwx.Station(
        "Ambient Weather Test Station",
        app_key=app_key,
        user_key=user_key,
        device_id=device_id,
    )


@pytest.mark.vcr()
def test_ambientwx_bad_api_key():
    """Verify bad Ambient Weather keys return properly."""

    station = ambientwx.Station(
        "Invalid Key",
        app_key="xyz123",
        user_key="456pqd",
        device_id="eb:8d:60:8a:33:e7",
    )

    assert station.current_conditions is None


@pytest.mark.vcr()
def test_ambientwx_conditions(station: ambientwx.Station):
    """Test current conditions from Ambient Weather."""

    conditions = station.current_conditions

    assert conditions is not None
    assert conditions.timestamp is not None
