/* Audio functions. */

import uPlot, { Options } from "uplot";
import "uplot/dist/uPlot.min.css";

interface Size {
  height: number;
  width: number;
}

export async function fetchSample(uri: URL): Promise<Float32Array> {
  const context = new AudioContext();
  const response = await fetch(uri);
  if (!response.ok) {
    throw Error(response.statusText);
  }
  const data = await context.decodeAudioData(await response.arrayBuffer());

  return data.getChannelData(0);
}

function getPlotSize(): Size {
  const width = Math.min(720, window.innerWidth - 100);
  return {
    width: Math.min(720, window.innerWidth),
    height: Math.floor(0.6 * width),
  };
}

export function playSample(
  sample: Float32Array,
  rate: number = 44_100
): AudioContext {
  const context = new AudioContext();
  const buffer = context.createBuffer(1, sample.length, rate);
  const source = context.createBufferSource();

  buffer.copyToChannel(sample, 0);
  source.buffer = buffer;
  source.connect(context.destination);
  source.start(0);

  return context;
}

// Check out https://github.com/skalinichev/uplot-wrappers.
export function plotSample(
  container: HTMLElement,
  sample: Float32Array,
  options: Options
): uPlot {
  const size = getPlotSize();
  const base: Options = {
    // More axis options at
    // https://github.com/leeoniya/uPlot/tree/master/docs#axis--grid-opts.
    axes: [{ grid: { show: false } }],
    cursor: {
      points: { show: false },
      x: false,
      y: false,
    },
    height: size.height,
    legend: {
      show: false,
    },
    scales: {
      x: {
        auto: true,
        time: false,
      },
      y: {
        auto: false,
        range: [-1, 1],
      },
    },
    series: [
      {
        label: "Index",
      },
      {
        label: "Amplitude",
        show: true,
        spanGaps: false,
        stroke: "purple",
        width: 1,
      },
    ],
    width: size.width,
  };

  const indices = [...Array(sample.length).keys()];
  const plot = new uPlot({ ...base, ...options }, [indices, sample], container);
  window.addEventListener("resize", (e) => {
    plot.setSize(getPlotSize());
  });

  return plot;
}
