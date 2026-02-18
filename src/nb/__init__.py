"""Personal collection of notebooks."""

import itertools
from enum import StrEnum
from typing import Any

import marimo
import numpy
from bokeh import layouts, plotting
from bokeh.models import Pane, Range1d
from bokeh.palettes import Category10
from marimo import Html
from marimo._runtime.state import State

from nb import source
from nb.source import Source, SourceFile, SourceInput

__version__ = "0.1.0"


class PlotKind(StrEnum):
    """Plot types."""

    Freq = "freq"
    Wave = "wave"


def audio_selector(default: str) -> tuple[State[Source], Html]:
    """Marimo input element to select an audio signal."""
    get_file, set_file = marimo.state(source.select(default))
    select = marimo.ui.dropdown(
        SourceFile.list(),
        allow_select_none=True,
        label="Select File",
        on_change=lambda name: set_file(SourceFile(name)),
        value=None,
    )
    synth_ = marimo.ui.dropdown(
        ["linear", "sine"],
        allow_select_none=True,
        label="Synth Generator",
        on_change=lambda name: set_file(source.select(name)),
        value=None,
    )
    upload = marimo.ui.file(
        filetypes=[".wav"],
        kind="button",
        label="Upload File",
        on_change=lambda input_: set_file(SourceInput(input_)),
    )
    return get_file, marimo.ui.batch(
        marimo.md("{select} {synth} {upload}"),
        {"select": select, "synth": synth_, "upload": upload},
    )


def plot(signals: list[dict], type: PlotKind = PlotKind.Wave, **kwargs: Any) -> Pane:  # noqa: A002
    """Plot audio signals with Bokeh."""
    match type:
        case PlotKind.Freq:
            return plot_freq(signals, **kwargs)
        case PlotKind.Wave:
            return plot_wave(signals, **kwargs)
        case _:
            message = f"Invalid choice '{type}' for PlotKind."
            raise ValueError(message)


def plot_freq(signals: list[dict], overlay: bool = True, **kwargs: Any) -> Pane:
    """Plot audio frequency spectrums with Bokeh."""
    palette = itertools.cycle(Category10[10])
    plots = []

    for signal in signals:
        rate = signal.pop("rate")
        sample = signal.pop("y")
        x = numpy.fft.rfftfreq(len(sample), 1 / rate)
        y = numpy.abs(numpy.fft.rfft(sample))
        color = signal.pop("color", next(palette))

        if overlay:
            if plots:
                plot = plots[0]
            else:
                plot = plotting.figure(
                    output_backend="webgl",
                    sizing_mode="stretch_width",
                    x_axis_label="Frequency (Hz)",
                    x_range=Range1d(0, 20_000),
                    y_axis_label="Amplitude",
                    **kwargs,
                )
                plots.append(plot)
        else:
            plot = plotting.figure(
                output_backend="webgl",
                sizing_mode="stretch_width",
                x_axis_label="Frequency (Hz)",
                x_range=Range1d(0, 20_000),
                y_axis_label="Amplitude",
                **kwargs,
            )
            plots.append(plot)

        plot.line(
            x=x,
            y=y,
            color=color,
            line_width=2,
            **signal,
        )
        plot.legend.click_policy = "mute"
        plot.toolbar.logo = None
    return layouts.row(plots, sizing_mode="stretch_width")


def plot_wave(signals: list[dict], overlay: bool = True, **kwargs: Any) -> Pane:
    """Plot audio waveform with Bokeh."""
    palette = itertools.cycle(Category10[10])
    x_range = Range1d(float("inf"), float("-inf"))
    plots = []

    for signal in signals:
        rate = signal.pop("rate")
        y = signal.pop("y")
        x = numpy.linspace(0, len(y) / rate, len(y))
        color = signal.pop("color", next(palette))
        x_range = Range1d(min(x[0], x_range.start), max(x[-1], x_range.end))

        if overlay:
            if plots:
                plot = plots[0]
                plot.x_range = x_range
            else:
                plot = plotting.figure(
                    output_backend="webgl",
                    sizing_mode="stretch_width",
                    x_axis_label="Time (s)",
                    x_range=Range1d(x[0], x[-1]),
                    y_axis_label="Amplitude",
                    y_range=Range1d(-1, 1),
                    **kwargs,
                )
                plots.append(plot)
        else:
            plot = plotting.figure(
                output_backend="webgl",
                sizing_mode="stretch_width",
                x_axis_label="Time (s)",
                x_range=Range1d(x[0], x[-1]),
                y_axis_label="Amplitude",
                y_range=Range1d(-1, 1),
                **kwargs,
            )
            plots.append(plot)

        plot.line(
            x=x,
            y=y,
            color=color,
            line_width=2,
            **signal,
        )
        plot.legend.click_policy = "mute"
        plot.toolbar.logo = None
    return layouts.row(plots, sizing_mode="stretch_width")
