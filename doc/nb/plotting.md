---
title: Plotting
marimo-version: 0.19.11
width: medium
header: |-
  # /// script
  # dependencies = [
  #   "numpy~=2.2",
  # ]
  # requires-python = ">=3.12.0,<4.0.0"
  #
  # [tool.uv.sources]
  # nb = { editable = true, path = "src/nb" }
  # ///
---

# Plotting

```python {.marimo}
import sys
if sys.platform == "emscripten":
    import micropip
    await micropip.install("/guides/data/nb-0.1.0-py3-none-any.whl")
import altair
import marimo as mo
import numpy
import plotly
import pyecharts
from altair import Chart
from bokeh import plotting
from bokeh.models import Range1d
from pandas import DataFrame
from plotly import express
from pyecharts.charts import Line
from pyecharts.options import AxisOpts, LabelOpts
import nb

altair.data_transformers.enable("vegafusion")
plotly.io.templates.default = "plotly_white"
```

```python {.marimo}
length = 48_000
# length = 480_000
# length = 2_880_000
times = numpy.linspace(0, 4*numpy.pi, length)
sines = numpy.sin(times)
delta = numpy.zeros(length)
delta[0] = 1
```

```python {.marimo}
# a_splot = (
#     Chart(DataFrame({"x": times, "y": sines}))
#     .mark_line().encode(x="x:Q", y="y:Q")
#     .interactive()
# )
# a_splot
```

```python {.marimo}
# a_dplot = (
#     Chart(DataFrame({"x": times, "y": delta}))
#     .mark_line().encode(x="x:Q", y="y:Q")
#     .interactive()
# )
# a_dplot
```

```python {.marimo}
b_splot = plotting.figure(
    output_backend="webgl",
    sizing_mode="stretch_width",
    x_axis_label="Time (s)",
    x_range=Range1d(times[0], times[-1]),
    y_axis_label="Amplitude",
    y_range=Range1d(-1, 1),
)
b_splot.line(
    x=times,
    y=sines,
    line_width=2,
)
b_splot.toolbar.logo = None
b_splot
```

```python {.marimo}
# b_dplot = plotting.figure(
#     output_backend="webgl",
#     sizing_mode="stretch_width",
#     x_axis_label="Time (s)",
#     x_range=Range1d(times[0], times[-1]),
#     y_axis_label="Amplitude",
#     y_range=Range1d(-1, 1),
# )
# b_dplot.line(
#     x=times,
#     y=delta,
#     line_width=2,
# )
# b_dplot.toolbar.logo = None
# b_dplot
```

```python {.marimo}
# from pyecharts import options as opts

# e_splot = (
#     Line()
#     .add_xaxis(times.tolist())
#     .add_yaxis("LegendFoo", sines.tolist(), is_symbol_show=False, label_opts=LabelOpts(is_show=False))
#     .set_global_opts(
#         datazoom_opts=[
#             opts.DataZoomOpts(type_="inside", xaxis_index=0),
#             opts.DataZoomOpts(type_="inside", yaxis_index=0),
#         ],
#         title_opts=opts.TitleOpts(title="Audio Signal"),
#         toolbox_opts=opts.ToolboxOpts(feature=opts.ToolBoxFeatureOpts(save_as_image=True)),
#     )
#     .set_global_opts(
#         xaxis_opts=opts.AxisOpts(
#             type_="value",
#             name="Time",
#             name_location="middle"
#         ),
#         yaxis_opts=opts.AxisOpts(
#             type_="value",
#             name="Amplitude",
#             name_location="middle",
#             min_=-1.0,
#             max_=1.0
#         )
#     )
# )
# e_splot
```

```python {.marimo}
p_splot = express.line(x=times, y=sines, render_mode="webgl", title="Waveform")
p_splot
```

```python {.marimo}
# p_dplot = express.line(x=times, y=delta, render_mode="webgl", title="Waveform")
# p_dplot
```
