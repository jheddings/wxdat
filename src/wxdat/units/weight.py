"""Working with weight quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity, UnitSymbol


class WeightUnit(UnitSymbol):
    """Symbols for weight units."""

    KILOGRAM = "kg"
    KILOGRAMS = "kg"
    KG = "kg"

    GRAM = "g"
    GRAMS = "g"
    G = "g"

    MILLIGRAM = "mg"
    MILLIGRAMS = "mg"
    MG = "mg"

    POUND = "lb"
    POUNDS = "lb"
    LB = "lb"

    OUNCE = "oz"
    OUNCES = "oz"
    OZ = "oz"

    TON = "ton"
    TONS = "tons"


class Weight(Quantity, ABC):
    """Base for all weight unit types."""

    @abstractproperty
    def kg(self):
        """Return the value of this quantity in kilograms."""

    @property
    def g(self):
        """Return the value of this quantity in grams."""
        return self.kg * 1000.0

    @property
    def mg(self):
        """Return the value of this quantity in milligrams."""
        return self.g * 1000.0

    @abstractproperty
    def lbs(self):
        """Return the value of this quantity in pounds."""

    @property
    def oz(self):
        """Return the value of this quantity in ounces."""
        return self.lbs * 16.0

    @property
    def ton(self):
        """Return the value of this quantity in tons."""
        return self.lbs / 2000.0


class Kilogram(Weight):
    """A quantity of weight in kilograms."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.KILOGRAM

    @property
    def kg(self):
        """Return the value of this quantity in kilograms."""
        return self.value

    @property
    def lbs(self):
        """Return the value of this quantity in pounds."""
        return self.kg * 2.20462262


class Gram(Kilogram):
    """A quantity of weight in grams."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.GRAM

    @property
    def kg(self):
        """Return the value of this quantity in kilograms."""
        return self.value / 1000


class Milligram(Kilogram):
    """A quantity of weight in milligrams."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.MILLIGRAM

    @property
    def kg(self):
        """Return the value of this quantity in kilograms."""
        return self.value / 1000000


class Pound(Weight):
    """A quantity of weight in pounds."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.POUND

    @property
    def kg(self):
        """Return the value of this quantity in kilograms."""
        return self.lbs * 0.45359237

    @property
    def lbs(self):
        """Return the value of this quantity in pounds."""
        return self.value


class Ounce(Pound):
    """A quantity of weight in ounces."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.OUNCE

    @property
    def lbs(self):
        """Return the value of this quantity in pounds."""
        return self.value / 16.0


class Ton(Pound):
    """A quantity of weight in standard (short) tons."""

    @property
    def symbol(self):
        """Return the unit symbol for this quantity."""
        return WeightUnit.TON

    @property
    def lbs(self):
        """Return the value of this quantity in pounds."""
        return self.value * 2000.0
