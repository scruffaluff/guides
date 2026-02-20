"""Mathematical functions."""

import numpy
from numpy.typing import NDArray
from tsdownsample import LTTBDownsampler


def downsample(x: NDArray, y: NDArray, limit: int = 8_192) -> tuple[NDArray, NDArray]:
    """Get indices for audio signal downsampling."""
    sampler = LTTBDownsampler()
    indices = sampler.downsample(x, y, n_out=limit)
    return x[indices], y[indices]


def loudness(signal: NDArray) -> NDArray:
    """Convert signal to decibels."""
    return 20 * numpy.log10(numpy.abs(signal))


def normalize(signal: NDArray) -> NDArray:
    """Scale signal -1 and +1 range."""
    return signal / numpy.abs(signal).max()
