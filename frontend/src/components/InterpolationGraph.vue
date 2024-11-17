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
    polynom: string,
    method?: string,
    xPoints: number[],
    yPoints: number[]
  }>();
  
  const chartCanvas = ref<HTMLCanvasElement | null>(null);
  const chartInstance = ref<Chart<'line', { x: number; y: number; }[], unknown> | null>(null);
  
  const generateLineData = (polynom: string) => {
    if (!polynom) {
      console.error("El polinomio no está definido.");
      return [];
    }

    if (props.method === 'spline') {
      const functions = polynom.slice(1, -1).split(',');
      const data = [];
      
      // Asegurarse de que los puntos estén ordenados
      const sortedPoints = props.xPoints.map((x, index) => ({
        x: x,
        y: props.yPoints[index]
      })).sort((a, b) => a.x - b.x);

      for (let i = 0; i < functions.length; i++) {
        const xStart = sortedPoints[i].x;
        const xEnd = sortedPoints[i + 1].x;
        
        const numPoints = 100;
        const step = (xEnd - xStart) / numPoints;
        
        for (let j = 0; j <= numPoints; j++) {
          const x = xStart + j * step;
          try {
            const y = eval(functions[i].trim().replace(/x/g, `(${x})`));
            data.push({ x, y });
          } catch (error) {
            console.error(`Error evaluating function at x=${x}:`, error);
          }
        }
      }
      
      return data;
    }

    // Para otros métodos (newton, lagrange, vandermonde)
    const sortedPoints = props.xPoints.map((x, index) => ({
      x: x,
      y: props.yPoints[index]
    })).sort((a, b) => a.x - b.x);

    const data = [];
    
    // Iterar sobre cada par de puntos consecutivos
    for (let i = 0; i < sortedPoints.length - 1; i++) {
      const xStart = sortedPoints[i].x;
      const xEnd = sortedPoints[i + 1].x;
      
      // Generar puntos para este segmento
      const numPoints = 100;
      const step = (xEnd - xStart) / numPoints;
      
      for (let j = 0; j <= numPoints; j++) {
        const x = xStart + j * step;
        try {
          const y = eval(polynom.replace(/x/g, `(${x})`));
          data.push({ x, y });
        } catch (error) {
          console.error(`Error evaluating function at x=${x}:`, error);
        }
      }
    }
    
    return data;
  };
  
  const generatePoints = (polynom: string) => {
    if (props.method === 'spline') {
      const points = [];
      const functions = polynom.slice(1, -1).split(',');
      
      // Generate points for each interval (from 1 to functions.length + 1)
      for (let i = 1; i <= functions.length + 1; i++) {
        try {
          // Evaluate the function at each integer point
          const y = eval(functions[i-1]?.trim().replace(/x/g, `(${i})`)) || 0;
          points.push({ x: i, y });
        } catch (error) {
          console.error(`Error evaluating point at x=${i}:`, error);
        }
      }
      return points;
    }
    return [];
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
          },
          {
            label: 'Points',
            data: props.xPoints.map((x, index) => ({
              x: x,
              y: props.yPoints[index]
            })),
            backgroundColor: 'blue',
            borderColor: 'blue',
            pointRadius: 5,
            pointHoverRadius: 7,
            showLine: false,
            order: 0,
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