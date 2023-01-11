"""Unit tests for the `units` module."""

# TODO compare values with conversion tables

import math

from wxdat import units
from wxdat.units.quantity import Quantity


def isclose(a, b):
    """Determine if the values are "close enough" for testing purposes."""
    return math.isclose(a, b, rel_tol=1e-5)


def assert_is_freezing(temp: units.temperature.Temperature):
    """Assert all values match expected levels for freezing."""
    assert temp.degC == 0.0
    assert temp.degF == 32.0
    assert temp.degK == 273.15


def test_basic_none():
    """Check that quantities of None behave as expected."""
    qty = Quantity(None)

    assert qty.value is None
    assert qty == None  # noqa: E711


def test_convert_none():
    """Make sure that conversions with None are also None."""
    tempC = units.degC(None)

    assert tempC.degC is None
    assert tempC.degF is None
    assert tempC.degK is None


def test_degC_freezing():
    """Confirm Celsius conversions for freezing."""
    tempC = units.degC(0)

    assert tempC == 0.0

    assert int(tempC) == 0
    assert float(tempC) == 0.0

    assert_is_freezing(tempC)


def test_degF_freezing():
    """Confirm Fahrenheit conversions for freezing."""
    tempF = units.degF(32)

    assert tempF == 32.0

    assert int(tempF) == 32
    assert float(tempF) == 32.0

    assert_is_freezing(tempF)


def test_degK_freezing():
    """Confirm Kelvin conversions for freezing."""
    tempK = units.degK(273.15)

    assert tempK == 273.15

    assert int(tempK) == 273
    assert float(tempK) == 273.15

    assert_is_freezing(tempK)


def test_boiling_temps():
    """Confirm conversions for boiling temperatures."""
    tempF = units.degF(212.0)
    assert tempF.degC == 100.0
    assert tempF.degK == 373.15

    tempC = units.degC(100.0)
    assert tempC.degF == 212.0
    assert tempF.degK == 373.15

    tempK = units.degK(373.15)
    assert tempK.degC == 100.0
    assert tempK.degF == 212.0


def test_one_meter():
    """Confirm simple Meter conversions."""
    meter = units.meter(1)

    assert meter == 1.0

    assert float(meter) == 1.0
    assert int(meter) == 1

    assert meter.kilometers == 0.001
    assert meter.centimeters == 100.0
    assert meter.millimeters == 1000.0

    assert isclose(meter.feet, 3.28084)
    assert isclose(meter.yards, 1.09361)
    assert isclose(meter.inches, 39.3701)


def test_more_meters():
    """Confirm additional Meter conversions."""
    assert isclose(units.meter(math.pi).feet, 10.3070628)


def test_one_mile():
    """Confirm simple Mile conversions."""
    mile = units.mile(1)

    assert mile == 1.0

    assert float(mile) == 1.0
    assert int(mile) == 1

    assert mile.feet == 5280.0
    assert mile.yards == 1760.0
    assert mile.inches == 63360.0

    assert mile.meters == 1609.344
    assert mile.kilometers == 1.609344


def test_more_miles():
    """Confirm additional Mile conversions."""
    assert isclose(units.mile(math.e).kilometers, 4.37465055)


def test_one_pascal():
    """Confirm simple Pascal conversions."""
    pa = units.Pa(1)

    assert pa == 1.0

    assert float(pa) == 1.0
    assert int(pa) == 1

    assert pa.bar == 1e-5
    assert isclose(pa.psi, 0.0001450377)


def test_one_hPa():
    """Confirm simple Hectopascal conversions."""
    hPa = units.hPa(1)

    assert hPa == 1.0

    assert float(hPa) == 1.0
    assert int(hPa) == 1

    assert hPa.bar == 1e-3

    assert isclose(hPa.inHg, 0.02953)


def test_one_inHg():
    """Confirm simple InchesMercury conversions."""
    inHg = units.inHg(1)

    assert inHg == 1.0

    assert float(inHg) == 1.0
    assert int(inHg) == 1

    assert isclose(inHg.bar, 0.033864)
    assert isclose(inHg.psi, 0.4911542)


def test_one_mps():
    """Confirm simple MetersPerSecond conversions."""
    mps = units.mps(1)

    assert mps == 1.0

    assert float(mps) == 1.0
    assert int(mps) == 1

    assert mps.kph == 3.6

    assert isclose(mps.mph, 2.23694)
    assert isclose(mps.fps, 3.28084)
    assert isclose(mps.knot, 1.94384449)


def test_one_kph():
    """Confirm simple KilometersPerHour conversions."""
    kph = units.kph(1)

    assert kph == 1.0

    assert float(kph) == 1.0
    assert int(kph) == 1

    assert isclose(kph.mps, 0.27777778)
    assert isclose(kph.mph, 0.62137119)
    assert isclose(kph.fps, 0.91134442)
    assert isclose(kph.knot, 0.5399568)


def test_one_mph():
    """Confirm simple MilesPerHour conversions."""
    mph = units.mph(1)

    assert mph == 1.0

    assert float(mph) == 1.0
    assert int(mph) == 1

    assert isclose(mph.fps, 1.466667)
    assert isclose(mph.mps, 0.44704)
    assert isclose(mph.kph, 1.609344)
    assert isclose(mph.knot, 0.8689762419)
