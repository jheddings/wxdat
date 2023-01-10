"""Methods and classes for converting between units."""


from .distance import Centimeter, Feet, Inch, Kilometer, Meter, Mile, Millimeter
from .pressure import Hectorpascal, InchesMercury, Pascal
from .temperature import Celsius, Fahrenheit, Kelvin
from .velocity import KilometersPerHour, MetersPerSecond, MilesPerHour


def m(value: float) -> Meter:
    """Return the given value as a Meter quantity."""
    return Meter(value)


def meter(value: float) -> Meter:
    """Return the given value as a Meter quantity."""
    return Meter(value)


def km(value: float) -> Kilometer:
    """Return the given value as a Kilometer quantity."""
    return Kilometer(value)


def cm(value: float) -> Centimeter:
    """Return the given value as a Centimeter quantity."""
    return Centimeter(value)


def mm(value: float) -> Millimeter:
    """Return the given value as a Millimeter quantity."""
    return Millimeter(value)


def mi(value: float) -> Mile:
    """Return the given value as a Mile quantity."""
    return Mile(value)


def mile(value: float) -> Mile:
    """Return the given value as a Mile quantity."""
    return Mile(value)


def inch(value: float) -> Inch:
    """Return the given value as an Inch quantity."""
    return Inch(value)


def ft(value: float) -> Feet:
    """Return the given value as Feet quantity."""
    return Feet(value)


def degC(value: float) -> Celsius:
    """Return the given value as Celsius quantity."""
    return Celsius(value)


def degF(value: float) -> Fahrenheit:
    """Return the given value as Fahrenheit quantity."""
    return Fahrenheit(value)


def degK(value: float) -> Kelvin:
    """Return the given value as Kelvin quantity."""
    return Kelvin(value)


def hPa(value: float) -> Hectorpascal:
    """Return the given value as Hectorpascal quantity."""
    return Hectorpascal(value)


def Pa(value: float) -> Pascal:
    """Return the given value as Pascal quantity."""
    return Pascal(value)


def inHg(value: float) -> InchesMercury:
    """Return the given value as InchesMercury quantity."""
    return InchesMercury(value)


def mps(value: float) -> MetersPerSecond:
    """Return the given value as MetersPerSecond quantity."""
    return MetersPerSecond(value)


def kph(value: float) -> KilometersPerHour:
    """Return the given value as KilometersPerHour quantity."""
    return KilometersPerHour(value)


def mph(value: float) -> MilesPerHour:
    """Return the given value as MilesPerHour quantity."""
    return MilesPerHour(value)
