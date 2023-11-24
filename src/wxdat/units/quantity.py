"""Base functionality for working with quantities."""

from typing import Union


def _other_value(other):
    """Return the value of `other` if it is a Quantity, otherwise return `other`."""
    if isinstance(other, Quantity):
        return other.value
    return other


class Quantity:
    """Base class for all quantities."""

    def __init__(self, value: Union[int, float]):
        self.value = value

    def __getattribute__(self, attr):
        """Return the requested attribute of this `Quantity`, or None.

        When callers request an attribute from a `Quantity` object, this method first
        examines the value of this `Quantity` object.  If the value is `None`, this
        method will always return `None` rather than accessing the requested attribute.

        The benefit of this approach is that subclasses do not need to check for `None`
        in each of the conversion methods.  For example, the `Temperature.degC()` method
        class does not need to cehck for `None` before computing the target value.

        NOTE - this does not affect the math (dunder) operations on `Quantity` objects.
        """

        # avoid recursion if `value` is requested ...
        if attr == "value":
            return super().__getattribute__("value")

        # ... if the contained value is None, return None
        if self.value is None:
            return None

        # otherwise, return the requested attribute
        return object.__getattribute__(self, attr)

    def __float__(self):
        """Return the Quantity value as a `float`."""
        return float(self.value)

    def __int__(self):
        """Return the Quantity value as an `int`."""
        return int(self.value)

    def __add__(self, other):
        """Return the sum of this `Quantity` and `other`."""
        return Quantity(self.value + _other_value(other))

    def __sub__(self, other):
        """Return the difference of this `Quantity` and `other`."""
        return Quantity(self.value - _other_value(other))

    def __mul__(self, other):
        """Return the product of this `Quantity` and `other`."""
        return Quantity(self.value * _other_value(other))

    def __truediv__(self, other):
        """Return the quotient of this `Quantity` and `other`."""
        return Quantity(self.value / _other_value(other))

    def __iadd__(self, other):
        """Add the given value to this Quantity."""
        self.value += _other_value(other)

        return self

    def __isub__(self, other):
        """Subtract the given value from this Number."""
        self.value -= _other_value(other)

        return self

    def __imul__(self, other):
        """Multiply this `Quantity` by `other`."""
        self.value *= _other_value(other)

        return self

    def __itruediv__(self, other):
        """Divide this `Quantity` by `other`."""
        self.value /= _other_value(other)

        return self

    def __eq__(self, other):
        """Determine if this `Quantity` value is equal to `other`."""
        return other == self.value

    def __ne__(self, other):
        """Determine if this property is not equal to the given object."""
        return other != self.value

    def __le__(self, other):
        """Return `True` if this `Quantity` value is less-than-or-equal-to `other`."""
        return self < other or self == other

    def __lt__(self, other):
        """Return `True` if this `Quantity` value is less-than `other`."""
        return other > self.value

    def __ge__(self, other):
        """Return `True` if this `Quantity` value is greater-than-or-equal-to `other`."""
        return self > other or self == other

    def __gt__(self, other):
        """Return `True` if this `Quantity` value is greater-than `other`."""
        return other < self.value

    def __str__(self):
        """Return a human readable string for this quantity."""
        return f"{self.value}"

    def __repr__(self):
        """Return a string representation of this quantity."""
        return str(self)
