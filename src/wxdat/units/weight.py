"""Working with weight quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Weight(Quantity, ABC):
    """Base for all weight unit types."""

    @abstractproperty
    def kg(self):
        """Return the value of this quantity in kilograms."""

    @property
    def g(self):
        """Return the value of this quantity in grams."""
        return self.kg * 1000.0

    @property
    def mg(self):
        """Return the value of this quantity in milligrams."""
        return self.g * 0.001

    @abstractproperty
    def lbs(self):
        """Return the value of this quantity in pounds."""

    @property
    def oz(self):
        """Return the value of this quantity in ounces."""
        return self.lbs * 16.0

    @property
    def ton(self):
        """Return the value of this quantity in tons."""
        return self.lbs * 2000.0
