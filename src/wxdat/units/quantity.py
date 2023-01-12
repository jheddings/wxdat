"""Base functionality for working with quantities."""

from typing import Union


class Quantity:
    """Base class for all quantities."""

    def __init__(self, value: Union[int, float]):
        self.value = value

    def __getattribute__(self, attr):
        """Return the requested attribute, or None.

        This method examines the value in this Quantity before computing the requested
        value.  If the internal value is None, this method always returns None.
        """

        # avoid recursion if `value` is requested ...
        if attr == "value":
            return super(Quantity, self).__getattribute__("value")

        # ... now we can access self.value for our check
        if self.value is None:
            return None

        return object.__getattribute__(self, attr)

    def __float__(self):
        """Return the Quantity value as a `float`."""
        return float(self.value)

    def __int__(self):
        """Return the Quantity value as an `int`."""
        return int(self.value)

    def __iadd__(self, other):
        """Add the given value to this Quantity.

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
        """Determine if this `Quantity` value is equal to `other`."""
        return other == self.value

    def __ne__(self, other):
        """Determine if this property is not equal to the given object."""
        return not self.__eq__(other)

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
        """Return a string representation of this quantity."""
        return f"{self.value}"

    def __repr__(self):
        """Return a string representation of this quantity."""
        return f"{self.value}"
