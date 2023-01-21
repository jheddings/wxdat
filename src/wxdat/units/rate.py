"""Working with rate quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Rate(Quantity, ABC):
    """Base for all rate unit types."""

    @abstractproperty
    def cmph(self):
        """Return the value of this quantity as centimeters per hour"""

    @property
    def mmph(self):
        """Return the value of this quantity as millimeters per hour"""
        return self.cmph * 10.0

    @property
    def inph(self):
        """Return the value of this quantity as inches per hour"""
        return self.cmph * 0.393700787


class CentimersPerHour(Rate):
    """A representation of cm / hour."""

    @property
    def cmph(self):
        """Return the value of this quantity as centimeters per second"""
        return self.value


class MillimetersPerHour(Rate):
    """A representation of mm / hour."""

    @property
    def cmph(self):
        """Return the value of this quantity as centimeters per second"""
        return self.value * 0.1


class InchesPerHour(Rate):
    """A representation of inch / hour."""

    @property
    def cmph(self):
        """Return the value of this quantity as centimeters per second"""
        return self.value * 2.54
