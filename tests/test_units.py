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


def test_one_kilometer():
    """Confirm simple Kilometer conversions."""
    kilo = units.km(1)

    assert kilo == 1.0

    assert float(kilo) == 1.0
    assert int(kilo) == 1

    assert kilo.meters == 1000.0

    assert isclose(kilo.miles, 0.62137119)
    assert isclose(kilo.feet, 3280.8399)


def test_one_millimeter():
    """Confirm simple Millimeter conversions."""
    mm = units.mm(1)

    assert mm == 1.0

    assert float(mm) == 1.0
    assert int(mm) == 1

    assert mm.meters == 0.001
    assert mm.centimeters == 0.1
    assert mm.kilometers == 1e-6

    assert isclose(mm.inches, 0.03937)
    assert isclose(mm.feet, 0.00328084)


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


def test_one_yard():
    """Confirm simple Yard conversions."""
    yard = units.yd(1)

    assert yard == 1.0

    assert float(yard) == 1.0
    assert int(yard) == 1

    assert yard.inches == 36.0
    assert isclose(yard.miles, 0.00056818)

    assert isclose(yard.meters, 0.9144)
    assert isclose(yard.centimeters, 91.44)


def test_one_foot():
    """Confirm simple Feet conversions."""
    foot = units.ft(1)

    assert foot == 1.0

    assert float(foot) == 1.0
    assert int(foot) == 1

    assert foot.inches == 12.0
    assert foot.centimeters == 30.48


def test_one_inch():
    """Confirm simple Inch conversions."""
    inch = units.inch(1)

    assert inch == 1.0

    assert float(inch) == 1.0
    assert int(inch) == 1

    assert isclose(inch.feet, 0.08333333)
    assert isclose(inch.yards, 0.02777778)
    assert isclose(inch.miles, 1.5782828e-5)

    assert inch.centimeters == 2.54
    assert inch.millimeters == 25.4


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


def test_one_fps():
    """Confirm simple FeetPerSecond conversions."""
    fps = units.fps(1)

    assert fps == 1.0

    assert float(fps) == 1.0
    assert int(fps) == 1

    assert isclose(fps.mps, 0.3048)
    assert isclose(fps.kph, 1.09728)
    assert isclose(fps.mph, 0.68181818)
    assert isclose(fps.knot, 0.5924838)


def test_one_mmph():
    """Confirm simple MillimeterPerHour conversions."""
    mmph = units.mmph(1)

    assert mmph == 1.0

    assert float(mmph) == 1.0
    assert int(mmph) == 1

    assert mmph.cmph == 0.1
    assert isclose(mmph.inph, 0.03937)
