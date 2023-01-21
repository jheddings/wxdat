"""Methods and classes for converting between units."""


from .distance import Centimeter, Feet, Inch, Kilometer, Meter, Mile, Millimeter, Yard
from .pressure import Hectopascal, InchesMercury, Pascal
from .rate import InchesPerHour, MillimetersPerHour
from .temperature import Celsius, Fahrenheit, Kelvin
from .velocity import FeetPerSecond, KilometersPerHour, MetersPerSecond, MilesPerHour


def meter(value: float) -> Meter:
    """Return the given value as a Meter quantity."""
    return Meter(value)


def m(value: float) -> Meter:
    """Return the given value as a Meter quantity."""
    return meter(value)


def km(value: float) -> Kilometer:
    """Return the given value as a Kilometer quantity."""
    return Kilometer(value)


def cm(value: float) -> Centimeter:
    """Return the given value as a Centimeter quantity."""
    return Centimeter(value)


def mm(value: float) -> Millimeter:
    """Return the given value as a Millimeter quantity."""
    return Millimeter(value)


def mile(value: float) -> Mile:
    """Return the given value as a Mile quantity."""
    return Mile(value)


def mi(value: float) -> Mile:
    """Return the given value as a Mile quantity."""
    return mile(value)


def inch(value: float) -> Inch:
    """Return the given value as an Inch quantity."""
    return Inch(value)


def ft(value: float) -> Feet:
    """Return the given value as Feet quantity."""
    return Feet(value)


def yd(value: float) -> Yard:
    """Return the given value as Feet Yard."""
    return Yard(value)


def degC(value: float) -> Celsius:
    """Return the given value as Celsius quantity."""
    return Celsius(value)


def degF(value: float) -> Fahrenheit:
    """Return the given value as Fahrenheit quantity."""
    return Fahrenheit(value)


def degK(value: float) -> Kelvin:
    """Return the given value as Kelvin quantity."""
    return Kelvin(value)


def hPa(value: float) -> Hectopascal:
    """Return the given value as Hectopascal quantity."""
    return Hectopascal(value)


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


def fps(value: float) -> FeetPerSecond:
    """Return the given value as FeetPerSecond quantity."""
    return FeetPerSecond(value)


def mmph(value: float) -> MillimetersPerHour:
    """Return the given value as MillimetersPerHour quantity."""
    return MillimetersPerHour(value)


def inph(value: float) -> InchesPerHour:
    """Return the given value as InchesPerHour quantity."""
    return InchesPerHour(value)
