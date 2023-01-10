"""Working with temperature quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Temperature(Quantity, ABC):
    """Base for all temperature unit types."""

    @abstractproperty
    def degC(self):
        """Return the value of this quantity as Celsius."""

    @abstractproperty
    def degF(self):
        """Return the value of this quantity as Fahrenheit."""

    @abstractproperty
    def degK(self):
        """Return the value of this quantity as Kelvin."""


class Celsius(Temperature):
    """A representation of Celsius."""

    @property
    def degC(self):
        """Return the value of this quantity as Celsius."""
        return self.value

    @property
    def degF(self):
        """Return the value of this quantity as Fahrenheit."""
        return (self.value * 1.8) + 32.0

    @property
    def degK(self):
        """Return the value of this quantity as Kelvin."""
        return self.value + 273.15


class Fahrenheit(Temperature):
    """A representation of Fahrenheit."""

    @property
    def degC(self):
        """Return the value of this quantity as Celsius."""
        return (self.value - 32.0) / 1.8

    @property
    def degF(self):
        """Return the value of this quantity as Fahrenheit."""
        return self.value

    @property
    def degK(self):
        """Return the value of this quantity as Kelvin."""
        return self.degC + 273.15


class Kelvin(Celsius):
    """A representation of Kelvin."""

    @property
    def degK(self):
        """Return the value of this quantity as Kelvin."""
        return self.value

    @property
    def degC(self):
        """Return the value of this quantity as Celsius."""
        return self.value - 273.15

    @property
    def degF(self):
        """Return the value of this quantity as Fahrenheit."""
        return (self.degC * 1.8) + 32.0
