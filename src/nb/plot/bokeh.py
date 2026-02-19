"""Plotting routines with Bokeh."""

import itertools
from typing import Any

import numpy
from bokeh import layouts, plotting
from bokeh.models import FixedTicker, Pane, Range1d
from bokeh.palettes import Category10

from nb import math


def frequency(signals: list[dict], overlay: bool = True, **kwargs: Any) -> Pane:
    """Plot audio frequency spectrums with Bokeh."""
    palette = itertools.cycle(Category10[10])
    plots = []

    for signal in signals:
        rate = signal.pop("rate")
        sample = signal.pop("y")
        x = numpy.fft.rfftfreq(len(sample), 1 / rate)
        y_ = numpy.fft.rfft(sample)
        y = math.loudness(y_ / numpy.abs(y_).max())
        color = signal.pop("color", next(palette))

        if overlay:
            if plots:
                plot = plots[0]
            else:
                plot = plotting.figure(
                    output_backend="webgl",
                    sizing_mode="stretch_width",
                    x_axis_label="Frequency (Hz)",
                    x_axis_type="log",
                    x_range=Range1d(1, 20_000),
                    y_axis_label="Loudness (dB)",
                    y_range=Range1d(-100, 0),
                    **kwargs,
                )
                plot.xaxis.ticker = FixedTicker(
                    ticks=[1, 50, 100, 500, 1_000, 5_000, 10_000, 15_000, 20_000]
                )
                plots.append(plot)
        else:
            plot = plotting.figure(
                output_backend="webgl",
                sizing_mode="stretch_width",
                x_axis_label="Frequency (Hz)",
                x_axis_type="log",
                x_range=Range1d(1, 20_000),
                y_axis_label="Loudness (dB)",
                y_range=Range1d(-100, 0),
                **kwargs,
            )
            plot.xaxis.ticker = FixedTicker(
                ticks=[1, 50, 100, 500, 1_000, 5_000, 10_000, 15_000, 20_000]
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


def waveform(signals: list[dict], overlay: bool = True, **kwargs: Any) -> Pane:
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
