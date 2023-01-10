"""Base functionality for working with quantities."""

from typing import Union


class Quantity:
    """Base class for all quantities."""

    def __init__(self, value: Union[int, float]):
        self.value = value

    def __float__(self):
        """Return the BaseUnit value as a `float`."""
        return float(self.value)

    def __int__(self):
        """Return the BaseUnit value as an `int`."""
        return int(self.value)

    def __iadd__(self, other):
        """Add the given value to this BaseUnit.

        The value may be either a native number type or another `Quantity` object.
        """

        if isinstance(other, Quantity):
            self.value += other.value
        else:
            self.value += other

        return self

    def __isub__(self, other):
        """Subtract the given value from this Number.

        The value may be either a native number type or another `Quantity` object.
        """

        if isinstance(other, Quantity):
            self.value -= other.value
        else:
            self.value -= other

        return self

    def __eq__(self, other):
        """Determine if this `BaseUnit` value is equal to `other`."""
        return other == self.value

    def __ne__(self, other):
        """Determine if this property is not equal to the given object."""
        return not self.__eq__(other)

    def __le__(self, other):
        """Return `True` if this `BaseUnit` value is less-than-or-equal-to `other`."""
        return self < other or self == other

    def __lt__(self, other):
        """Return `True` if this `BaseUnit` value is less-than `other`."""
        return other > self.value

    def __ge__(self, other):
        """Return `True` if this `BaseUnit` value is greater-than-or-equal-to `other`."""
        return self > other or self == other

    def __gt__(self, other):
        """Return `True` if this `BaseUnit` value is greater-than `other`."""
        return other < self.value

    def __str__(self):
        """Return a string representation of this quantity."""
        return f"{self.value}"

    def __repr__(self):
        """Return a string representation of this quantity."""
        return f"{self.value}"
