"""Personal collection of notebooks."""

import contextlib
import itertools
import sys
from collections.abc import Iterator
from enum import StrEnum
from io import BytesIO
from pathlib import Path
from typing import Any, BinaryIO
from urllib import request

import marimo
import numpy
from bokeh import plotting
from bokeh.models import Plot, Range1d
from bokeh.palettes import Category10
from marimo import ui
from numpy.typing import NDArray
from scipy.io import wavfile

__version__ = "0.1.0"

File = str | Path | ui.file


class PlotType(StrEnum):
    """Signal plot options."""

    Freq = "freq"
    Wave = "wave"


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
                url = str(folder.parent / f"data/audio/{name}")
                yield BytesIO(request.urlopen(url).read())  # noqa: S310
            else:
                path = folder.parents[1] / f"data/audio/{name}"
                handle = open(path, "rb")  # noqa: PTH123, SIM115
                yield handle
    finally:
        if handle:
            handle.close()


def normalize(signal: NDArray) -> NDArray:
    """Scale signal -1 and +1 range."""
    return signal / numpy.abs(signal).max()


def plot(signals: list[dict], type: PlotType = PlotType.Wave, **kwargs: Any) -> Plot:  # noqa: A002
    """Plot audio signals with Bokeh."""
    match type:
        case PlotType.Freq:
            return plot_freq(signals, **kwargs)
        case PlotType.Wave:
            return plot_wave(signals, **kwargs)
        case _:
            message = f"Value '{type}' is not a valid PlotType."
            raise ValueError(message)


def plot_freq(signals: list[dict], **kwargs: Any) -> Plot:
    """Plot audio frequency spectrums with Bokeh."""
    palette = itertools.cycle(Category10[10])
    plot = plotting.figure(
        output_backend="webgl",
        sizing_mode="stretch_width",
        x_axis_label="Frequency (Hz)",
        x_range=Range1d(0, 20_000),
        y_axis_label="Amplitude",
        **kwargs,
    )

    for signal in signals:
        rate = signal.pop("rate")
        sample = signal.pop("y")
        x = numpy.fft.rfftfreq(len(sample), 1 / rate)
        y = numpy.abs(numpy.fft.rfft(sample))

        color = signal.pop("color", next(palette))
        plot.line(
            x=x,
            y=y,
            color=color,
            line_width=2,
            **signal,
        )

    plot.legend.click_policy = "mute"
    plot.toolbar.logo = None
    return plot


def plot_wave(signals: list[dict], **kwargs: Any) -> Plot:
    """Plot audio waveform with Bokeh."""
    palette = itertools.cycle(Category10[10])
    plot = plotting.figure(
        output_backend="webgl",
        sizing_mode="stretch_width",
        x_axis_label="Time (s)",
        y_axis_label="Amplitude",
        y_range=Range1d(-1, 1),
        **kwargs,
    )

    for signal in signals:
        rate = signal.pop("rate")
        y = signal.pop("y")
        x = numpy.linspace(0, len(y) / rate, len(y))

        color = signal.pop("color", next(palette))
        plot.line(
            x=x,
            y=y,
            color=color,
            line_width=2,
            **signal,
        )

    plot.legend.click_policy = "mute"
    plot.toolbar.logo = None
    return plot


def read_signal(name: File) -> tuple[NDArray, NDArray, int]:
    """Load audio file from path, URL, or Marimo input."""
    with open_file(name) as file:
        rate, signal = wavfile.read(file)
    if len(signal.shape) > 1:
        signal = numpy.mean(signal, axis=1)
    times = numpy.arange(len(signal)) / rate
    return times, normalize(signal), rate
