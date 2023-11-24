"""Utilities for testing."""

import math

COMPARE_TOLERANCE = 1e-5


def isclose(a, b):
    """Determine if the values are "close enough" for testing purposes."""
    return math.isclose(a, b, rel_tol=COMPARE_TOLERANCE)
