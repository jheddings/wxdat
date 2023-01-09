"""Methods for converting between units."""


def degC__degF(val: float) -> float:
    """Convert Celcius to Farenheit."""

    if val is None:
        return None

    return val * 1.8 + 32.0


def mm__in(val: float) -> float:
    """Convert millimeters to inches."""

    if val is None:
        return None

    return val / 25.4


def meter__mile(val: float) -> float:
    """Convert meters to miles."""

    if val is None:
        return None

    return val / 1609.344


def mps__mph(val: float) -> float:
    """Convert meters/sec to miles/hour."""

    if val is None:
        return None

    return val * 2.2369362921


def Pa__inHg(val: float) -> float:
    """Convert Pascal to inches-mercury."""

    if val is None:
        return None

    return val / 3386.3886666667


def hPa__inHg(val: float) -> float:
    """Convert Hectorpascal to inches-mercury."""

    if val is None:
        return None

    return Pa__inHg(val * 1000.0)
