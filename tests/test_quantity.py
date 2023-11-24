"""Unit tests for the `units` module."""

import pytest

from wxdat.units.quantity import Quantity


def test_basic_none():
    """Check that quantities of None behave as expected."""
    qty = Quantity(None)

    assert qty.value is None
    assert qty == None  # noqa: E711


def test_none_math():
    """Check that math with None behaves as expected."""
    qty = Quantity(None)

    with pytest.raises(TypeError):
        qty + 1

    with pytest.raises(TypeError):
        qty *= 1

    with pytest.raises(TypeError):
        float(qty)

    with pytest.raises(TypeError):
        Quantity(1) - None


def test_qty_zero():
    """Check that Quantity(0) behaves as expected."""
    qty = Quantity(0)

    assert qty.value == 0
    assert qty == 0
    assert qty == 0.0
    assert qty == Quantity(0)

    assert qty + 0 == 0
    assert qty - 0 == 0
    assert qty * 1 == 0
    assert qty / 1 == 0


def test_qty_iadd():
    """Check that Quantity.__iadd__ works as expected."""
    qty_a = Quantity(1)

    # using a scalar
    qty_a += 1

    assert qty_a == 2

    # using a Quantity object
    qty_b = Quantity(1)

    qty_a += qty_b

    assert qty_a == 3
    assert qty_b == 1


def test_qty_isub():
    """Check that Quantity.__isub__ works as expected."""
    qty_a = Quantity(10)

    # using a scalar
    qty_a -= 1

    assert qty_a == 9

    # using a Quantity object
    qty_b = Quantity(4)

    qty_a -= qty_b

    assert qty_a == 5
    assert qty_b == 4


def test_qty_imul():
    """Check that Quantity.__imul__ works as expected."""
    qty_a = Quantity(2)

    # using a scalar
    qty_a *= 2

    assert qty_a == 4

    # using a Quantity object
    qty_b = Quantity(3)

    qty_a *= qty_b

    assert qty_a == 12
    assert qty_b == 3


def test_qty_idiv():
    """Check that Quantity.__itruediv__ works as expected."""
    qty_a = Quantity(10)

    # using a scalar
    qty_a /= 2

    assert qty_a == 5

    # using a Quantity object
    qty_b = Quantity(2)

    qty_a /= qty_b

    assert qty_a == 2.5
    assert qty_b == 2


def test_qty_equality():
    """Check that Quantity.__eq__ works as expected."""
    qty_a = Quantity(1)

    assert qty_a == 1
    assert qty_a == 1.0
    assert qty_a == Quantity(1)

    assert qty_a != -1
    assert qty_a != 0.0
    assert qty_a != Quantity(-1)


def test_qty_less_than():
    """Check that Quantity.__lt__ and Quantity.__le__ work as expected."""
    qty_a = Quantity(1)

    # using scalars
    assert qty_a < 2.0
    assert qty_a <= 1.0 and qty_a <= 2.0
    assert 2.0 > qty_a

    # using Quantity objects
    assert qty_a < Quantity(2)
    assert qty_a <= Quantity(1) and qty_a <= Quantity(2)


def test_qty_greater_than():
    """Check that Quantity.__gt__ and Quantity.__ge__ work as expected."""
    qty_a = Quantity(1)

    # using scalars
    assert qty_a > 0.0
    assert qty_a >= 1.0 and qty_a >= 0.0
    assert 0.0 < qty_a

    # using Quantity objects
    assert qty_a > Quantity(0)
    assert qty_a >= Quantity(1) and qty_a >= Quantity(0)
