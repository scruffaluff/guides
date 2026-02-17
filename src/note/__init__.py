"""Personal collection of notebooks."""

import contextlib
import itertools
import sys
from collections.abc import Iterator
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO
from urllib import request

import marimo
import numpy
from bokeh import plotting
from bokeh.models import Plot, Range1d
from bokeh.palettes import Category20
from marimo import ui
from numpy.typing import NDArray
from scipy.io import wavfile

__version__ = "0.1.0"

File = str | Path | ui.file


@contextlib.contextmanager
def open_file(name: File) -> Iterator[BinaryIO]:
    """Get binary file handle for path, URL, or Marimo input."""
    handle = None
    try:
        if isinstance(name, ui.file):
            yield BytesIO(name.contents() or b"")
        else:
            folder = marimo.notebook_location()
            if folder is None:
                message = "Unable to find notebook location."
                raise ValueError(message)
            elif sys.platform == "emscripten":
                url = str(folder.parent / f"file/{name}")
                yield BytesIO(request.urlopen(url).read())  # noqa: S310
            else:
                path = folder.parent / f"data/public/file/{name}"
                handle = open(path, "rb")  # noqa: PTH123, SIM115
                yield handle
    finally:
        if handle:
            handle.close()


def normalize(signal: NDArray) -> NDArray:
    """Scale signal -1 and +1 range."""
    return signal / numpy.abs(signal).max()


def plot_signals(signals: list[dict], **kwargs: Any) -> Plot:
    """Plot multiple audio signals with Bokeh."""
    palette = itertools.cycle(Category20[20])
    plot = plotting.figure(
        output_backend="webgl",
        sizing_mode="stretch_width",
        x_axis_label="Time (s)",
        y_axis_label="Amplitude",
        y_range=Range1d(-1, 1),
        **kwargs,
    )
    plot.toolbar.logo = None

    for signal in signals:
        color = signal.pop("color", next(palette))
        plot.line(
            color=color,
            line_width=2,
            **signal,
        )
    return plot


def read_signal(name: File) -> tuple[NDArray, NDArray, int]:
    """Load audio file from path, URL, or Marimo input."""
    with open_file(name) as file:
        rate, signal = wavfile.read(file)
    if len(signal.shape) > 1:
        signal = numpy.mean(signal, axis=1)
    times = numpy.arange(len(signal)) / rate
    return times, normalize(signal), rate
