"""Mathematical functions."""

import numpy
from numpy.typing import NDArray


def normalize(signal: NDArray) -> NDArray:
    """Scale signal -1 and +1 range."""
    return signal / numpy.abs(signal).max()
