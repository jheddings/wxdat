"""Unit tests for volume units."""

from conftest import isclose

from wxdat import units


def test_one_liter():
    """Confirm simple Liter conversions."""
    liter = units.L(1)

    assert liter == 1.0

    assert float(liter) == 1.0
    assert int(liter) == 1

    assert liter.L == 1.0
    assert liter.mL == 1000.0

    assert isclose(liter.gal, 0.2641720524)
    assert isclose(liter.pint, 2.1133764189)
    assert isclose(liter.quart, 1.0566882094)
    assert isclose(liter.us_oz, 33.814022702)

    assert str(liter) == "1 L"
    assert repr(liter) == "Liter(1)"


def test_one_ml():
    """Confirm simple Milliliter conversions."""
    ml = units.ml(1)

    assert ml == 1.0

    assert float(ml) == 1.0
    assert int(ml) == 1

    assert ml.mL == 1.0
    assert ml.L == 0.001

    assert isclose(ml.us_oz, 0.0338140227)

    assert str(ml) == "1 mL"
    assert repr(ml) == "Milliliter(1)"


def test_one_gal():
    """Confirm simple Gallon conversions."""
    gal = units.gal(1)

    assert gal == 1.0

    assert float(gal) == 1.0
    assert int(gal) == 1

    assert gal.gal == 1.0
    assert gal.pint == 8.0
    assert gal.quart == 4.0
    assert gal.us_oz == 128.0

    assert isclose(gal.L, 3.78541178)
    assert isclose(gal.mL, 3785.41178)

    assert str(gal) == "1 gal"
    assert repr(gal) == "Gallon(1)"


def test_one_pint():
    """Confirm simple Pint conversions."""
    pint = units.pint(1)

    assert pint == 1.0

    assert float(pint) == 1.0
    assert int(pint) == 1

    assert pint.pint == 1.0
    assert pint.quart == 0.5
    assert pint.us_oz == 16.0

    assert isclose(pint.L, 0.473176473)
    assert isclose(pint.mL, 473.176473)

    assert str(pint) == "1 pt"
    assert repr(pint) == "Pint(1)"


def test_one_quart():
    """Confirm simple Quart conversions."""
    quart = units.quart(1)

    assert quart == 1.0

    assert float(quart) == 1.0
    assert int(quart) == 1

    assert quart.quart == 1.0
    assert quart.us_oz == 32.0

    assert isclose(quart.L, 0.946352946)
    assert isclose(quart.mL, 946.352946)

    assert str(quart) == "1 qt"
    assert repr(quart) == "Quart(1)"


def test_one_us_oz():
    """Confirm simple US fluid ounce conversions."""
    fl_oz = units.us_oz(1)

    assert fl_oz == 1.0

    assert float(fl_oz) == 1.0
    assert int(fl_oz) == 1

    assert fl_oz.pint == 0.0625
    assert fl_oz.quart == 0.03125
    assert fl_oz.gal == 0.0078125

    assert isclose(fl_oz.L, 0.0295735296)
    assert isclose(fl_oz.mL, 29.5735295625)

    assert str(fl_oz) == "1 fl oz"
    assert repr(fl_oz) == "FluidOunceUS(1)"
