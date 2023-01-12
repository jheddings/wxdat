"""Working with volume quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Volume(Quantity, ABC):
    """Base for all volume unit types."""

    @abstractproperty
    def liters(self):
        """Return the value of this quantity in liters."""

    @abstractproperty
    def milliliters(self):
        """Return the value of this quantity in milliliters."""

    @abstractproperty
    def gallons(self):
        """Return the value of this quantity in gallons."""

    @abstractproperty
    def pints(self):
        """Return the value of this quantity in pints."""

    @abstractproperty
    def quarts(self):
        """Return the value of this quantity in quarts."""

    @abstractproperty
    def us_oz(self):
        """Return the value of this quantity in US fluid ounces."""

    @abstractproperty
    def uk_oz(self):
        """Return the value of this quantity in UK fluid ounces."""
