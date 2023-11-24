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
    assert liter.ml == 1000.0

    assert isclose(liter.gal, 0.2641720524)
    assert isclose(liter.pint, 2.1133764189)
    assert isclose(liter.quart, 1.0566882094)
    assert isclose(liter.us_oz, 33.814022702)


def test_one_ml():
    """Confirm simple Milliliter conversions."""
    ml = units.ml(1)

    assert ml == 1.0

    assert float(ml) == 1.0
    assert int(ml) == 1

    assert ml.ml == 1.0
    assert ml.L == 0.001

    assert isclose(ml.us_oz, 0.0338140227)


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
    assert isclose(gal.ml, 3785.41178)
