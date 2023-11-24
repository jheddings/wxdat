"""Working with volume quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity, UnitSymbol


class VolumeUnit(UnitSymbol):
    """Symbols for volume units."""

    LITER = "L"
    LITERS = "L"
    L = "L"

    MILLILITER = "mL"
    MILLILITERS = "mL"
    ML = "mL"

    GALLON = "gal"
    GALLONS = "gal"
    GAL = "gal"

    PINT = "pt"
    PINTS = "pt"
    PT = "pt"

    QUART = "qt"
    QUARTS = "qt"
    QT = "qt"

    US_FLUID_OUNCE = "fl oz"
    US_FLUID_OUNCES = "fl oz"
    US_FL_OZ = "fl oz"
    US_OZ = "fl oz"


class Volume(Quantity, ABC):
    """Base for all volume unit types."""

    @abstractproperty
    def L(self):
        """Return the value of this quantity in liters."""

    @property
    def mL(self):
        """Return the value of this quantity in milliliters."""
        return self.L * 1000.0

    @abstractproperty
    def gal(self):
        """Return the value of this quantity in gallons."""

    @property
    def pint(self):
        """Return the value of this quantity in pints."""
        return self.gal * 8.0

    @property
    def quart(self):
        """Return the value of this quantity in quarts."""
        return self.gal * 4.0

    @property
    def us_oz(self):
        """Return the value of this quantity in US fluid ounces."""
        return self.gal * 128.0


class Liter(Volume):
    """A quantity of volume in liters."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.LITER

    @property
    def L(self):
        """Return the value of this quantity in liters."""
        return self.value

    @property
    def gal(self):
        """Return the value of this quantity in gallons."""
        return self.L * 0.2641720524


class Milliliter(Liter):
    """A quantity of volume in milliliters."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.MILLILITER

    @property
    def L(self):
        """Return the value of this quantity in liters."""
        return self.value / 1000


class Gallon(Liter):
    """A quantity of volume in gallons."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.GALLON

    @property
    def L(self):
        """Return the value of this quantity in liters."""
        return self.gal * 3.785411784

    @property
    def gal(self):
        """Return the value of this quantity in gallons."""
        return self.value


class Pint(Gallon):
    """A quantity of volume in pints."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.PINT

    @property
    def gal(self):
        """Return the value of this quantity in gallons."""
        return self.value / 8.0


class Quart(Gallon):
    """A quantity of volume in quarts."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.QUART

    @property
    def gal(self):
        """Return the value of this quantity in gallons."""
        return self.value / 4.0


class FluidOunceUS(Gallon):
    """A quantity of volume in fluid ounces (US)."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return VolumeUnit.US_FLUID_OUNCE

    @property
    def gal(self):
        """Return the value of this quantity in gallons."""
        return self.value / 128.0
