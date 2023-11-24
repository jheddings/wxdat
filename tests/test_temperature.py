"""Unit tests for temperature units."""

from wxdat import units


def assert_is_freezing(temp: units.temperature.Temperature):
    """Assert all values match expected levels for freezing."""
    assert temp.degC == 0.0
    assert temp.degF == 32.0
    assert temp.degK == 273.15


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

    assert str(tempC) == "0 °C"
    assert repr(tempC) == "Celsius(0)"

    assert_is_freezing(tempC)


def test_degF_freezing():
    """Confirm Fahrenheit conversions for freezing."""
    tempF = units.degF(32)

    assert tempF == 32.0

    assert int(tempF) == 32
    assert float(tempF) == 32.0

    assert str(tempF) == "32 °F"
    assert repr(tempF) == "Fahrenheit(32)"

    assert_is_freezing(tempF)


def test_degK_freezing():
    """Confirm Kelvin conversions for freezing."""
    tempK = units.degK(273.15)

    assert tempK == 273.15

    assert int(tempK) == 273
    assert float(tempK) == 273.15

    assert str(tempK) == "273.15 K"
    assert repr(tempK) == "Kelvin(273.15)"

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
