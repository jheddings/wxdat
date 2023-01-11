"""Unit tests for the `units` module."""

# TODO compare values with conversion tables

import math

from wxdat import units


def isclose(a, b):
    """Determine if the values are "close enough" for testing purposes."""
    return math.isclose(a, b, rel_tol=1e-5)


def assert_is_freezing(temp: units.temperature.Temperature):
    assert temp.degC == 0.0
    assert temp.degF == 32.0
    assert temp.degK == 273.15


def test_degC():
    tempC = units.degC(0)

    assert tempC == 0.0

    assert int(tempC) == 0
    assert float(tempC) == 0.0

    assert_is_freezing(tempC)


def test_degF():
    tempF = units.degF(32)

    assert tempF == 32.0

    assert int(tempF) == 32
    assert float(tempF) == 32.0

    assert_is_freezing(tempF)


def test_degK():
    tempK = units.degK(273.15)

    assert tempK == 273.15

    assert int(tempK) == 273
    assert float(tempK) == 273.15

    assert_is_freezing(tempK)


def test_meters():
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


def test_miles():
    mile = units.mile(1)

    assert mile == 1.0

    assert float(mile) == 1.0
    assert int(mile) == 1

    assert mile.feet == 5280.0
    assert mile.yards == 1760.0
    assert mile.inches == 63360.0

    assert mile.meters == 1609.344
    assert mile.kilometers == 1.609344
