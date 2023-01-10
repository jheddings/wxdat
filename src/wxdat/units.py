"""Methods and classes for converting between units."""


from abc import ABC, abstractproperty
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
        """Add the given value to this BaseUnit."""

        if isinstance(other, Quantity):
            self.value += other.value
        else:
            self.value += other

        return self

    def __isub__(self, other):
        """Subtract the given value from this Number."""

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


class Pressure(Quantity, ABC):
    """Base for all pressure unit types."""

    @abstractproperty
    def hPa(self):
        """Return the value of this quantity as Hectorpascals."""

    @abstractproperty
    def Pa(self):
        """Return the value of this quantity as Pascals."""

    @abstractproperty
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""


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


class Pascal(Pressure):
    """A representation of Pascals."""

    @property
    def hPa(self):
        """Return the value of this quantity as Hectorpascals."""
        return self.value / 1000.0

    @property
    def Pa(self):
        """Return the value of this quantity as Pascals."""
        return self.value

    @property
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""
        return self.value / 3386.3886666667


class Hectorpascal(Pascal):
    """A representation of Hectorpascals."""

    def __init__(self, value):
        super().__init__(value * 1000.0)


class InchesMercury(Pressure):
    """A representation of InchesMercury."""

    @property
    def hPa(self):
        """Return the value of this quantity as Hectorpascals."""
        return self.Pa / 1000.0

    @property
    def Pa(self):
        """Return the value of this quantity as Pascals."""
        return self.value / 3386.3886666667

    @property
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""
        return self.value


def m(value: float) -> Meter:
    """Return the given value as a Meter."""
    return Meter(value)


def meter(value: float) -> Meter:
    """Return the given value as a Meter."""
    return Meter(value)


def km(value: float) -> Kilometer:
    """Return the given value as a Kilometer."""
    return Kilometer(value)


def cm(value: float) -> Centimeter:
    """Return the given value as a Centimeter."""
    return Centimeter(value)


def mm(value: float) -> Millimeter:
    """Return the given value as a Millimeter."""
    return Millimeter(value)


def mile(value: float) -> Mile:
    """Return the given value as a Mile."""
    return Mile(value)


def inch(value: float) -> Inch:
    """Return the given value as an Inch."""
    return Inch(value)


def ft(value: float) -> Feet:
    """Return the given value as Feet."""
    return Feet(value)


def foot(value: float) -> Feet:
    """Return the given value as Feet."""
    return Feet(value)


def feet(value: float) -> Feet:
    """Return the given value as Feet."""
    return Feet(value)


def degC(value: float) -> Celsius:
    """Return the given value as Celsius."""
    return Celsius(value)


def degF(value: float) -> Fahrenheit:
    """Return the given value as Fahrenheit."""
    return Fahrenheit(value)


def degK(value: float) -> Kelvin:
    """Return the given value as Kelvin."""
    return Kelvin(value)


def hPa(value: float) -> Hectorpascal:
    """Return the given value as Hectorpascal."""
    return Hectorpascal(value)


def Pa(value: float) -> Pascal:
    """Return the given value as Pascal."""
    return Pascal(value)


def pascal(value: float) -> Pascal:
    """Return the given value as Pascal."""
    return Pascal(value)


def inHg(value: float) -> InchesMercury:
    """Return the given value as InchesMercury."""
    return InchesMercury(value)


def mps(value: float) -> MetersPerSecond:
    """Return the given value as MetersPerSecond."""
    return MetersPerSecond(value)


def kph(value: float) -> KilometersPerHour:
    """Return the given value as KilometersPerHour."""
    return KilometersPerHour(value)


def mph(value: float) -> MilesPerHour:
    """Return the given value as MilesPerHour."""
    return MilesPerHour(value)
