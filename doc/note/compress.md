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
    await micropip.install("/guides/file/note-1.0.0-py3-none-any.whl")
import marimo as mo
import numpy
from numpy.typing import NDArray
import note
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
    disabled=not edit.value,
    language="python",
)
code
```

```python {.marimo}
edit = mo.ui.switch(label="Edit")
ratio = mo.ui.slider(0, 10, 0.1, label="Ratio", show_value=True, value=4.0)
threshold = mo.ui.slider(0, 1, 0.01, label="Threshold", show_value=True, value=0.8)
file = mo.ui.file(filetypes=[".wav"], kind="button", label="Audio")
mo.hstack([mo.hstack([edit, ratio, threshold], gap=1, justify="start"), file])
```

```python {.marimo}
path = file if file.value else "bongo_high_pitch.wav"
times, signal, rate = note.read_signal(path)
```

```python {.marimo}
mo.stop(edit.value)
exec(f"{code.value}\nprocessed = note.normalize(compress(signal))")
plot = note.plot_signals([
    {"x": times, "y": signal, "legend_label": "original"},
    {"x": times, "y": processed, "legend_label": "compressed"},
    ],
    title="Compression",
)
plot
```

```python {.marimo}
mo.hstack([mo.audio(signal, rate), mo.audio(processed, rate)], gap=2, justify="start")
```
