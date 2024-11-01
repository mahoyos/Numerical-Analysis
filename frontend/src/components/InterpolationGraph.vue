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
    polynom: string
  }>();
  
  const chartCanvas = ref<HTMLCanvasElement | null>(null);
  const chartInstance = ref<Chart<'line', { x: number; y: number; }[], unknown> | null>(null);
  
  const generateLineData = (polynom: string) => {
    if (!polynom) {
      console.error("El polinomio no está definido.");
      return [];
    }
    const data = [];
    for (let x = -100; x <= 100; x += 0.1) {
      const y = eval(polynom.replace(/x/g, `(${x})`)); // Evaluar la función
      data.push({ x, y });
    }
    return data;
  };
  
  const createChart = () => {
    if (chartCanvas.value) {
      const ctx = chartCanvas.value.getContext('2d');
      if (ctx) {
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
            label: 'Function',
            data: generateLineData(props.polynom),
            borderColor: 'red',
            fill: false,
            order: 1,
          }
        ];
  
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
      console.error("El canvas no está disponible.");
    }
  };
  
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