"""Unit tests for distance units."""

import math

from conftest import isclose

from wxdat import units


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
