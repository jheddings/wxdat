"""Unit tests for the `units` module."""

from wxdat.units.quantity import Quantity


def test_basic_none():
    """Check that quantities of None behave as expected."""
    qty = Quantity(None)

    assert qty.value is None
    assert qty == None  # noqa: E711
