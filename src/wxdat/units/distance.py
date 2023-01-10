"""Working with distance quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Distance(Quantity, ABC):
    """Base for all distance unit types."""

    @abstractproperty
    def meters(self):
        """Return the value of this quantity in meters."""

    @abstractproperty
    def kilometers(self):
        """Return the value of this quantity in kilometers."""

    @abstractproperty
    def centimeters(self):
        """Return the value of this quantity in centimeters."""

    @abstractproperty
    def millimeters(self):
        """Return the value of this quantity in millimeters."""

    @abstractproperty
    def miles(self):
        """Return the value of this quantity in miles."""

    @abstractproperty
    def feet(self):
        """Return the value of this quantity in feet."""

    @abstractproperty
    def inches(self):
        """Return the value of this quantity in inches."""

    @abstractproperty
    def yards(self):
        """Return the value of this quantity in yards."""


class Meter(Distance):
    """A representation of a meter."""

    @property
    def meters(self):
        return self.value

    @property
    def kilometers(self):
        """Return the value of this quantity in kilometers."""
        return self.meters / 1000.0

    @property
    def centimeters(self):
        """Return the value of this quantity in centimeters."""
        return self.meters * 100.0

    @property
    def millimeters(self):
        """Return the value of this quantity in millimeters."""
        return self.meters * 1000.0

    @property
    def miles(self):
        """Return the value of this quantity in miles."""
        return self.kilometers * 0.6213711922

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.meters * 3.28084

    @property
    def inches(self):
        """Return the value of this quantity in inches."""
        return self.meters * 39.37

    @property
    def yards(self):
        """Return the value of this quantity in yards."""
        return self.meters * 1.0936132983


class Millimeter(Meter):
    """A representation of a millimeter."""

    @property
    def meters(self):
        return self.value / 1000.0


class Centimeter(Meter):
    """A representation of a centimeter."""

    @property
    def meters(self):
        return self.value / 100.0


class Kilometer(Meter):
    """A representation of a kilometer."""

    @property
    def meters(self):
        return self.value * 1000.0


class Feet(Distance):
    """A representation of feet."""

    @property
    def meters(self):
        return self.feet * 1609.344

    @property
    def kilometers(self):
        """Return the value of this quantity in kilometers."""
        return self.meters / 1000.0

    @property
    def centimeters(self):
        """Return the value of this quantity in centimeters."""
        return self.meters * 100.0

    @property
    def millimeters(self):
        """Return the value of this quantity in millimeters."""
        return self.meters * 1000.0

    @property
    def miles(self):
        """Return the value of this quantity in miles."""
        return self.feet / 5280.0

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value

    @property
    def inches(self):
        """Return the value of this quantity in inches."""
        return self.feet * 12.0

    @property
    def yards(self):
        """Return the value of this quantity in yards."""
        return self.feet / 3.0


class Mile(Feet):
    """A representation of a mile."""

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value * 5280.0


class Yard(Feet):
    """A representation of a yard."""

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value * 3.0


class Inch(Feet):
    """A representation of an inch."""

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value / 12.0
