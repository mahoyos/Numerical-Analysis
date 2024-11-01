<template>
  <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex justify-content-between align-items-center">
          <h6 class="m-0 font-weight-bold text-primary">Chart</h6>
          <div>
              <button @click="resetZoom" class="btn btn-secondary btn-sm mr-3">
                  Reset Zoom
              </button>
              <button @click="downloadChart" class="btn btn-primary btn-sm">
                  Download SVG
              </button>
          </div>
      </div>
      <div class="chart-container">
      <canvas ref="chartCanvas"></canvas>
      </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart, registerables } from 'chart.js';
import type { ChartOptions } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import { DownloadChartUtils } from '../util/DownloadChartUtils';

Chart.register(...registerables, zoomPlugin);

const props = defineProps<{
  matrixValues: number[][],
  solutionVector: number[],
  matrixSize: number
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
const chartInstance = ref<Chart<'line', { x: number; y: number; }[], unknown> | null>(null);

const generateLineData = (a: number, b: number, c: number) => {
  const data = [];
  for (let x = -100; x <= 100; x += 0.1) {
    if (b !== 0) {
      const y = (c - a * x) / b;
      data.push({ x, y });
    }
  }
  return data;
};

const calculateIntersection = (a1: number, b1: number, c1: number, a2: number, b2: number, c2: number) => {
  const determinant = a1 * b2 - a2 * b1;
  if (determinant === 0) {
    return null;
  }
  const x = (c1 * b2 - c2 * b1) / determinant;
  const y = (a1 * c2 - a2 * c1) / determinant;
  return { x, y };
};

const createChart = () => {
  if (chartCanvas.value && props.matrixSize === 2) {
    const ctx = chartCanvas.value.getContext('2d');
    if (ctx) {
      const [a1, b1] = props.matrixValues[0];
      const [a2, b2] = props.matrixValues[1];
      const [c1, c2] = props.solutionVector;

      const intersection = calculateIntersection(a1, b1, c1, a2, b2, c2);

      const options: ChartOptions<'line'> = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            min: -10,
            max: 10,
          },
          y: {
            min: -10,
            max: 10,
          }
        },
        plugins: {
          zoom: {
            zoom: {
              wheel: { enabled: true },
              pinch: { enabled: true },
              mode: 'xy',
            },
            pan: {
              enabled: true,
              mode: 'xy',
            },
          },
          tooltip: {
            callbacks: {
              label: function(context) {
                const x = context.raw.x.toFixed(2);
                const y = context.raw.y.toFixed(2);
                return `(${x}, ${y})`;
              }
            }
          }
        },
      };

      const datasets = [
        {
          label: 'Line 1',
          data: generateLineData(a1, b1, c1),
          borderColor: 'red',
          fill: false,
          order: 1,
        },
        {
          label: 'Line 2',
          data: generateLineData(a2, b2, c2),
          borderColor: 'blue',
          fill: false,
          order: 1,
        }
      ];

      if (intersection) {
        const formattedIntersection = {
          x: parseFloat(intersection.x.toFixed(2)),
          y: parseFloat(intersection.y.toFixed(2))
        };

        datasets.push({
          label: 'Intersection',
          data: [formattedIntersection],
          borderColor: 'green',
          backgroundColor: 'green',
          pointRadius: 10,
          type: 'scatter',
          showLine: false,
          order: 0,
        });
      }

      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: datasets,
        },
        options: options,
      });
    } else {
      console.error("No se pudo obtener el contexto del canvas.");
    }
  } else {
    console.error("El canvas no está disponible o el tamaño de la matriz no es 2.");
  }
};

const updateChart = () => {
  if (chartInstance.value && props.matrixSize === 2) {
    const [a1, b1] = props.matrixValues[0];
    const [a2, b2] = props.matrixValues[1];
    const [c1, c2] = props.solutionVector;

    const newData1 = generateLineData(a1, b1, c1);
    const newData2 = generateLineData(a2, b2, c2);

    if (JSON.stringify(chartInstance.value.data.datasets[0].data) !== JSON.stringify(newData1) ||
        JSON.stringify(chartInstance.value.data.datasets[1].data) !== JSON.stringify(newData2)) {
      chartInstance.value.data.datasets[0].data = newData1;
      chartInstance.value.data.datasets[1].data = newData2;
      chartInstance.value.update();
    }
  }
};

watch(() => [props.matrixValues, props.solutionVector], updateChart, { deep: true });
onMounted(createChart);

const resetZoom = () => {
if (chartInstance.value) {
  chartInstance.value.resetZoom();
}
};

const downloadChart = () => {
if (chartCanvas.value) {
  DownloadChartUtils.downloadSVG(chartCanvas.value, 'function-chart.svg');
}
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 500px;
  position: relative;
}
</style>