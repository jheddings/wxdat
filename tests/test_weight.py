"""Unit tests for weight units."""

from conftest import isclose

from wxdat import units


def test_one_kg():
    """Confirm simple Kilogram conversions."""
    kg = units.kg(1)

    assert kg == 1.0

    assert float(kg) == 1.0
    assert int(kg) == 1

    assert kg.kg == 1.0
    assert kg.g == 1000.0
    assert kg.mg == 1000000.0

    assert isclose(kg.lbs, 2.204622)
    assert isclose(kg.oz, 35.274)


def test_one_g():
    """Confirm simple Gram conversions."""
    g = units.g(1)

    assert g == 1.0

    assert float(g) == 1.0
    assert int(g) == 1

    assert g.kg == 0.001
    assert g.g == 1.0
    assert g.mg == 1000.0

    assert isclose(g.lbs, 0.002204622)
    assert isclose(g.oz, 0.035274)


def test_one_lb():
    """Confirm simple Pound conversions."""
    lb = units.lb(1)

    assert lb == 1.0

    assert float(lb) == 1.0
    assert int(lb) == 1

    assert lb.lbs == 1.0
    assert lb.oz == 16.0
    assert lb.ton == 0.0005

    assert isclose(lb.kg, 0.45359237)


def test_one_oz():
    """Confirm simple Ounce conversions."""
    oz = units.oz(1)

    assert oz == 1.0

    assert float(oz) == 1.0
    assert int(oz) == 1

    assert oz.oz == 1.0
    assert oz.lbs == 0.0625
    assert oz.ton == 0.00003125

    assert isclose(oz.kg, 0.02834952)
