"""Unit tests for the `units` module."""

# TODO compare values with conversion tables

from wxdat import units


def test_degC():
    tempC = units.degC(0)

    assert tempC == 0.0

    assert int(tempC) == 0
    assert float(tempC) == 0.0

    assert tempC.degC == 0.0
    assert tempC.degF == 32.0


def test_degF():
    tempF = units.degF(32)

    assert tempF == 32.0

    assert int(tempF) == 32
    assert float(tempF) == 32.0

    assert tempF.degC == 0.0
    assert tempF.degF == 32.0


def test_degK():
    tempK = units.degK(273.15)

    assert tempK == 273.15

    assert int(tempK) == 273
    assert float(tempK) == 273.15

    assert tempK.degC == 0.0
    assert tempK.degF == 32.0


def test_meters():
    meter = units.meter(1)

    assert meter == 1.0

    assert float(meter) == 1.0
    assert int(meter) == 1

    assert meter.kilometers == 0.001
    assert meter.centimeters == 100.0
    assert meter.millimeters == 1000.0


def test_miles():
    mile = units.mile(1)

    assert mile == 1.0

    assert float(mile) == 1.0
    assert int(mile) == 1

    assert mile.feet == 5280.0
    assert mile.yards == 1760.0
    assert mile.inches == 63360.0
