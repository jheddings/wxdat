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

    @abstractproperty
    def fps(self):
        """Return the value of this quantity as feet per second"""

    @abstractproperty
    def knot(self):
        """Return the value of this quantity as knots"""


class MetersPerSecond(Velocity):
    """A representation of m/s."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return self.value

    @property
    def kph(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.mps * 3.6

    @property
    def mph(self):
        """Return the value of this quantity as miles per hour"""
        return self.mps * 2.2369363

    @property
    def fps(self):
        """Return the value of this quantity as feet per second"""
        return self.mps * 3.28084

    @property
    def knot(self):
        """Return the value of this quantity as knots"""
        return self.mps * 1.943844


class KilometersPerHour(MetersPerSecond):
    """A representation of km/h."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return (self.value * 1000.0) / 3600.0


class MilesPerHour(Velocity):
    """A representation of mph."""

    @property
    def mps(self):
        """Return the value of this quantity as meters per second"""
        return self.mph * 0.44704

    @property
    def kph(self):
        """Return the value of this quantity as kilometers per hour"""
        return self.mph * 1.609344

    @property
    def mph(self):
        """Return the value of this quantity as miles per hour"""
        return self.value

    @property
    def fps(self):
        """Return the value of this quantity as feet per second"""
        return (self.mph * 5280.0) / 3600.0

    @property
    def knot(self):
        """Return the value of this quantity as knots"""
        return self.mph * 0.86897624


class FeetPerSecond(MilesPerHour):
    """A representation of fps."""

    @property
    def mph(self):
        """Return the value of this quantity as miles per hour"""
        return (self.value * 3600.0) / 5280.0
