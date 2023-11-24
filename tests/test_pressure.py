"""Unit tests for pressure units."""

from conftest import isclose

from wxdat import units


def test_one_pascal():
    """Confirm simple Pascal conversions."""
    pa = units.Pa(1)

    assert pa == 1.0

    assert float(pa) == 1.0
    assert int(pa) == 1

    assert pa.bar == 1e-5
    assert isclose(pa.psi, 0.0001450377)

    assert str(pa) == "1 Pa"
    assert repr(pa) == "Pascal(1)"


def test_one_hPa():
    """Confirm simple Hectopascal conversions."""
    hPa = units.hPa(1)

    assert hPa == 1.0

    assert float(hPa) == 1.0
    assert int(hPa) == 1

    assert hPa.bar == 1e-3

    assert isclose(hPa.inHg, 0.02953)

    assert str(hPa) == "1 hPa"
    assert repr(hPa) == "Hectopascal(1)"


def test_one_inHg():
    """Confirm simple InchesMercury conversions."""
    inHg = units.inHg(1)

    assert inHg == 1.0

    assert float(inHg) == 1.0
    assert int(inHg) == 1

    assert isclose(inHg.bar, 0.033864)
    assert isclose(inHg.psi, 0.4911542)

    assert str(inHg) == "1 inHg"
    assert repr(inHg) == "InchesMercury(1)"
