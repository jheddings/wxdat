"""Methods and classes for converting between units."""


from .distance import Centimeter, Foot, Inch, Kilometer, Meter, Mile, Millimeter, Yard
from .pressure import Hectopascal, InchesMercury, Pascal
from .rate import InchesPerHour, MillimetersPerHour
from .temperature import Celsius, Fahrenheit, Kelvin
from .velocity import FeetPerSecond, KilometersPerHour, MetersPerSecond, MilesPerHour
from .volume import FluidOunceUS, Gallon, Liter, Milliliter, Pint, Quart
from .weight import Gram, Kilogram, Milligram, Ounce, Pound, Ton


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


def ft(value: float) -> Foot:
    """Return the given value as a Feet quantity."""
    return Foot(value)


def yd(value: float) -> Yard:
    """Return the given value as a Feet Yard."""
    return Yard(value)


def degC(value: float) -> Celsius:
    """Return the given value as a Celsius quantity."""
    return Celsius(value)


def degF(value: float) -> Fahrenheit:
    """Return the given value as a Fahrenheit quantity."""
    return Fahrenheit(value)


def degK(value: float) -> Kelvin:
    """Return the given value as a Kelvin quantity."""
    return Kelvin(value)


def hPa(value: float) -> Hectopascal:
    """Return the given value as a Hectopascal quantity."""
    return Hectopascal(value)


def Pa(value: float) -> Pascal:
    """Return the given value as a Pascal quantity."""
    return Pascal(value)


def inHg(value: float) -> InchesMercury:
    """Return the given value as a InchesMercury quantity."""
    return InchesMercury(value)


def mps(value: float) -> MetersPerSecond:
    """Return the given value as a MetersPerSecond quantity."""
    return MetersPerSecond(value)


def kph(value: float) -> KilometersPerHour:
    """Return the given value as a KilometersPerHour quantity."""
    return KilometersPerHour(value)


def mph(value: float) -> MilesPerHour:
    """Return the given value as a MilesPerHour quantity."""
    return MilesPerHour(value)


def fps(value: float) -> FeetPerSecond:
    """Return the given value as a FeetPerSecond quantity."""
    return FeetPerSecond(value)


def mmph(value: float) -> MillimetersPerHour:
    """Return the given value as a MillimetersPerHour quantity."""
    return MillimetersPerHour(value)


def inph(value: float) -> InchesPerHour:
    """Return the given value as a InchesPerHour quantity."""
    return InchesPerHour(value)


def kg(value: float) -> Kilogram:
    """Return the given value as a Kilogram quantity."""
    return Kilogram(value)


def g(value: float) -> Gram:
    """Return the given value as a Gram quantity."""
    return Gram(value)


def mg(value: float) -> Milligram:
    """Return the given value as a Milligram quantity."""
    return Milligram(value)


def lb(value: float) -> Pound:
    """Return the given value as a Pound quantity."""
    return Pound(value)


def oz(value: float) -> Ounce:
    """Return the given value as a Ounce quantity."""
    return Ounce(value)


def ton(value: float) -> Ton:
    """Return the given value as a Ton quantity."""
    return Ton(value)


def L(value: float) -> Liter:
    """Return the given value as a Liter quantity."""
    return Liter(value)


def ml(value: float) -> Milliliter:
    """Return the given value as a Milliliter quantity."""
    return Milliliter(value)


def gal(value: float) -> Gallon:
    """Return the given value as a Gallon quantity."""
    return Gallon(value)


def pint(value: float) -> Pint:
    """Return the given value as a Pint quantity."""
    return Pint(value)


def quart(value: float) -> Quart:
    """Return the given value as a Quart quantity."""
    return Quart(value)


def us_oz(value: float) -> FluidOunceUS:
    """Return the given value as a FluidOunceUS quantity."""
    return FluidOunceUS(value)
