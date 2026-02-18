---
title: Compression
marimo-version: 0.19.11
width: medium
header: |-
  # /// script
  # dependencies = [
  #   "bokeh~=3.6",
  #   "numpy~=2.2",
  #   "scipy~=1.14.0",
  # ]
  # requires-python = ">=3.12.0,<4.0.0"
  #
  # [tool.uv.sources]
  # nb = { editable = true, path = "src/nb" }
  # ///
---

# Compression

```python {.marimo name="setup"}
import sys
if sys.platform == "emscripten":
    import micropip
    await micropip.install("/guides/data/nb-0.1.0-py3-none-any.whl")
import marimo as mo
import numpy
from numpy.typing import NDArray
import nb
from nb import PlotType
```

Dynamic range compressors decrease an audio signal's dynamic range by
attenuating loud samples and amplifying quiet samples.

Compressor parameters:

- _Threshold_ is the minimum amplitude for compression to be applied.
- _Ratio_ is the amount of compression to be applied.
- _Attack_ is how quickly compression is applied.
- _Release_ is how quickly compression falls off.
- _Make gain_ is additional gain applied to the entire signal.
- _Knee width_ smooths the compression to ensure differentiability at the
  threshold.

The compression algorithm for this tutorial is implemented with the following
code.

```python {.marimo}
code = mo.ui.code_editor(
    value=f"""
def compress(
    signal: NDArray,
    knee_width: float = 0.0,
    make_gain: float = 0.0,
    ratio: float = {ratio.value},
    threshold: float = {threshold.value},
) -> NDArray:
    sign = numpy.sign(signal)
    amplitude = numpy.abs(signal)

    for index in range(len(signal)):
        value = amplitude[index] - threshold
        if value > knee_width / 2:
            amplitude[index] = value / ratio + threshold
        elif value > -knee_width / 2:
            smoothing = (value + knee_width / 2) ** 2 / (2 * knee_width)
            amplitude[index] += (1 / ratio - 1) * smoothing

    return sign * (amplitude + make_gain)
    """.strip(),
    language="python",
    debounce=True,
)
code
```

```python {.marimo}
overlay = mo.ui.switch(label="Overlay", value=True)
type_ = mo.ui.dropdown(["Freq", "Wave"], allow_select_none=False, label="Type", value="Wave")
ratio = mo.ui.slider(0, 10, 0.1, label="Ratio", show_value=True, value=4.0)
threshold = mo.ui.slider(0, 1, 0.01, label="Threshold", show_value=True, value=0.8)
file = mo.ui.file(filetypes=[".wav"], kind="button", label="Audio")

mo.ui.tabs(
    {
        "Inputs": mo.hstack([file, ratio, threshold], gap=2, justify="start"),
        "Visuals": mo.hstack([type_, overlay], gap=2, justify="start"),
    },
    label="Controls"
)
```

```python {.marimo}
path = file if file.value else "templeofhades-scratch_sample.wav"
title = path.name() if file.value else path
times, signal, rate = nb.read_signal(path)
exec(f"{code.value}\nprocessed = nb.normalize(compress(signal))")
```

```python {.marimo}
plot = nb.plot([
    {"rate": rate, "y": signal, "legend_label": "original"},
    {"rate": rate, "y": processed, "legend_label": "compressed"},
    ],
    overlay=overlay.value,
    title=title,
    type=PlotType(type_.value.lower()),
)
plot
```

We can listen to both versions of the signal below.

```python {.marimo}
mo.hstack([mo.vstack([mo.md("### Original"), mo.audio(signal, rate)]), mo.vstack([mo.md("### Compressed"), mo.audio(processed, rate)])], gap=2, justify="start")
```

```python {.marimo}

```
