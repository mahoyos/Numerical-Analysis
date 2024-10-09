<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import { Chart, ChartOptions, registerables } from 'chart.js';
import zoomPlugin from 'chartjs-plugin-zoom';
import { evaluate, parse } from 'mathjs';
import ExpressionUtils from '../util/ChartUtils';
import { DownloadChartUtils } from '../util/DownloadChartUtils';

Chart.register(...registerables, zoomPlugin);

const props = defineProps<{
  functionExpression: string;
  solution: number;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
const chartInstance = ref<Chart | null>(null);

const generateChartData = (start: number, end: number, step: number) => {
  const parsedExpression = parse(ExpressionUtils.sanitizeExpression(props.functionExpression));
  return Array.from({ length: Math.floor((end - start) / step) + 1 }, (_, i) => {
    const x = start + i * step;
    const y = parsedExpression.evaluate({ x: x });
    return { x, y };
  });
};

const createChart = () => {
  if (chartCanvas.value) {
    const ctx = chartCanvas.value.getContext('2d');
    if (ctx) {
      const range = 20; 
      const start = Math.floor(props.solution - range);
      const end = Math.ceil(props.solution + range);
      const step = 0.1;

      const options: ChartOptions<'line'> = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          x: {
            type: 'linear',
            position: 'bottom',
            min: start,
            max: end,
            grid: {
              color: (context) => context.tick.value === 0 ? 'rgba(0, 0, 0, 1)' : 'rgba(0, 0, 0, 0.1)',
            },
          },
          y: {
            min: - 10,
            max: 10,
            grid: {
              color: (context) => context.tick.value === 0 ? 'rgba(0, 0, 0, 1)' : 'rgba(0, 0, 0, 0.1)',
            },
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
        },
      };

      chartInstance.value = new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'Function',
              data: generateChartData(start, end, step),
              borderColor: 'blue',
              fill: false,
            },
            {
              label: 'Solution Point',
              data: [{ 
                x: props.solution, 
                y: parse(ExpressionUtils.sanitizeExpression(props.functionExpression)).evaluate({ x: props.solution }) 
              }],
              borderColor: 'red',
              backgroundColor: 'red',
              pointRadius: 5,
              pointHoverRadius: 8,
              showLine: false,
              order : 1,
            },
          ],
        },
        options: options,
      });
    }
  }
};

const updateChart = () => {
  if (chartInstance.value) {
    const range = 20;
    const start = Math.floor(props.solution - range);
    const end = Math.ceil(props.solution + range);
    const step = 0.1;

    chartInstance.value.data.datasets[0].data = generateChartData(start, end, step);
    chartInstance.value.data.datasets[1].data = [{
      x: props.solution,
      y: parse(ExpressionUtils.sanitizeExpression(props.functionExpression)).evaluate({ x: props.solution })
    }];

    chartInstance.value.update();
  }
};

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

onMounted(() => {
  createChart();
});

watch(() => [props.functionExpression, props.solution], () => {
  updateChart();
});
</script>

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
    <div class="card-body">
      <div class="chart-container">
        <canvas ref="chartCanvas"></canvas>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden; 
  width: 100%;
  height: 500px;
  position: relative;
}
</style>
