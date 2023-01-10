"""Working with velocity quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Velocity(Quantity, ABC):
    """Base for all velocity unit types."""

    @abstractproperty
    def mps(self):
        """Return the value of this quantity as meters per second"""

    @abstractproperty
    def kph(self):
        """Return the value of this quantity as kilometers per hour"""

    @abstractproperty
    def mph(self):
        """Return the value of this quantity as miles per hour"""


class MetersPerSecond(Velocity):
    """A representation of m/s."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return self.value

    @property
    def kph(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.mps / 3.6

    @property
    def mph(self):
        """Return the value of this quantity as miles per hour"""
        return self.mps * 2.237


class KilometersPerHour(Velocity):
    """A representation of km/h."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return self.value * 3.6


class MilesPerHour(Velocity):
    """A representation of mph."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return self.mph / 2.237

    @property
    def kph(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.mph * 1.609344

    @property
    def mph(self):
        """Return the value of this quantity as miles per hour"""
        return self.value
