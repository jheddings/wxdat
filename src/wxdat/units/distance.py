"""Working with distance quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity, UnitSymbol


class DistanceUnit(UnitSymbol):
    """Symbols for distance units."""

    METER = "m"
    METERS = "m"
    M = "m"

    KILOMETER = "km"
    KILOMETERS = "km"
    KM = "km"

    CENTIMETER = "cm"
    CENTIMETERS = "cm"
    CM = "cm"

    MILLIMETER = "mm"
    MILLIMETERS = "mm"
    MM = "mm"

    MILE = "mi"
    MILES = "mi"
    MI = "mi"

    FOOT = "ft"
    FEET = "ft"
    FT = "ft"

    INCH = "in"
    INCHES = "in"
    IN = "in"

    YARD = "yd"
    YARDS = "yd"
    YD = "yd"


class Distance(Quantity, ABC):
    """Base for all distance unit types."""

    @abstractproperty
    def meters(self):
        """Return the value of this quantity in meters."""

    @property
    def kilometers(self):
        """Return the value of this quantity in kilometers."""
        return self.meters * 0.001

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

    @abstractproperty
    def feet(self):
        """Return the value of this quantity in feet."""

    @property
    def inches(self):
        """Return the value of this quantity in inches."""
        return self.feet * 12.0

    @property
    def yards(self):
        """Return the value of this quantity in yards."""
        return self.feet / 3.0

    @property
    def knots(self):
        """Return the value of this quantity in nautical miles."""
        return self.feet * 0.00016458

    @property
    def parsecs(self):
        """Return the value of this quantity in parsecs (because we can)."""
        return self.miles * 5.2155286735076e-14


class Meter(Distance):
    """A representation of a meter."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.METER

    @property
    def meters(self):
        return self.value

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
        return self.meters * 39.37007874

    @property
    def yards(self):
        """Return the value of this quantity in yards."""
        return self.meters * 1.0936132983


class Millimeter(Meter):
    """A representation of a millimeter."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.MILLIMETER

    @property
    def meters(self):
        return self.value * 0.001


class Centimeter(Meter):
    """A representation of a centimeter."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.CENTIMETER

    @property
    def meters(self):
        return self.value * 0.01


class Kilometer(Meter):
    """A representation of a kilometer."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.KILOMETER

    @property
    def meters(self):
        return self.value * 1000.0


class Foot(Distance):
    """A representation of foot measurements."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.FOOT

    @property
    def meters(self):
        return self.feet * 0.3048

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value


class Mile(Foot):
    """A representation of a mile."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.MILE

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value * 5280.0


class Yard(Foot):
    """A representation of a yard."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.YARD

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value * 3.0


class Inch(Foot):
    """A representation of an inch."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return DistanceUnit.INCH

    @property
    def feet(self):
        """Return the value of this quantity in feet."""
        return self.value / 12.0
