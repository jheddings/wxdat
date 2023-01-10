"""Working with pressure quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


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
