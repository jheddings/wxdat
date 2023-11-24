"""Unit tests for velocity units."""

from conftest import isclose

from wxdat import units


def test_one_mps():
    """Confirm simple MetersPerSecond conversions."""
    mps = units.mps(1)

    assert mps == 1.0

    assert float(mps) == 1.0
    assert int(mps) == 1

    assert mps.kph == 3.6

    assert isclose(mps.mph, 2.23694)
    assert isclose(mps.fps, 3.28084)
    assert isclose(mps.knot, 1.94384449)


def test_one_kph():
    """Confirm simple KilometersPerHour conversions."""
    kph = units.kph(1)

    assert kph == 1.0

    assert float(kph) == 1.0
    assert int(kph) == 1

    assert isclose(kph.mps, 0.27777778)
    assert isclose(kph.mph, 0.62137119)
    assert isclose(kph.fps, 0.91134442)
    assert isclose(kph.knot, 0.5399568)


def test_one_mph():
    """Confirm simple MilesPerHour conversions."""
    mph = units.mph(1)

    assert mph == 1.0

    assert float(mph) == 1.0
    assert int(mph) == 1

    assert isclose(mph.fps, 1.466667)
    assert isclose(mph.mps, 0.44704)
    assert isclose(mph.kph, 1.609344)
    assert isclose(mph.knot, 0.8689762419)


def test_one_fps():
    """Confirm simple FeetPerSecond conversions."""
    fps = units.fps(1)

    assert fps == 1.0

    assert float(fps) == 1.0
    assert int(fps) == 1

    assert isclose(fps.mps, 0.3048)
    assert isclose(fps.kph, 1.09728)
    assert isclose(fps.mph, 0.68181818)
    assert isclose(fps.knot, 0.5924838)


def test_one_mmph():
    """Confirm simple MillimeterPerHour conversions."""
    mmph = units.mmph(1)

    assert mmph == 1.0

    assert float(mmph) == 1.0
    assert int(mmph) == 1

    assert mmph.cmph == 0.1
    assert isclose(mmph.inph, 0.03937)
