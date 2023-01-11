"""Working with pressure quantities."""

from abc import ABC, abstractproperty

from .quantity import Quantity


class Pressure(Quantity, ABC):
    """Base for all pressure unit types."""

    @property
    def bar(self):
        """Return the value of this quantity as bar."""
        return self.hPa * 0.001

    @property
    def hPa(self):
        """Return the value of this quantity as Hectopascals."""
        return self.Pa * 0.01

    @abstractproperty
    def Pa(self):
        """Return the value of this quantity as Pascals."""

    @abstractproperty
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""

    @abstractproperty
    def psi(self):
        """Return the value of this quantity as pounds-per-square-inch."""


class Pascal(Pressure):
    """A representation of Pascals."""

    @property
    def Pa(self):
        """Return the value of this quantity as Pascals."""
        return self.value

    @property
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""
        return self.Pa / 3386.3886666667

    @property
    def psi(self):
        """Return the value of this quantity as pounds-per-square-inch."""
        return self.Pa / 6894.75729


class Hectopascal(Pascal):
    """A representation of Hectopascals."""

    @property
    def Pa(self):
        """Return the value of this quantity as Pascals."""
        return self.value * 100


class InchesMercury(Pressure):
    """A representation of InchesMercury."""

    @property
    def Pa(self):
        """Return the value of this quantity as Pascals."""
        return self.inHg * 3386.3886666667

    @property
    def inHg(self):
        """Return the value of this quantity as inches-mercury."""
        return self.value

    @property
    def psi(self):
        """Return the value of this quantity as pounds-per-square-inch."""
        return self.inHg * 0.4911541996322
