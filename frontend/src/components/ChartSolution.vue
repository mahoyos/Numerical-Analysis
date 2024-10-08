<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { evaluate } from 'mathjs';
import ExpressionUtils from '../util/ChartUtils';
import { DownloadChartUtils } from '../util/DownloadChartUtils';

Chart.register(...registerables);

const props = defineProps<{
    functionExpression: string;
    solution: number;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);
const chartContainer = ref<HTMLElement | null>(null);

onMounted(() => {
    if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d');
        if (ctx) {
            const range = 20;
            const start = Math.floor(props.solution - range);
            const end = Math.ceil(props.solution + range);
            const step = 0.1;

            const data = Array.from({ length: Math.floor((end - start) / step) + 1 }, (_, i) => {
                    const x = start + i * step;
                    const y = evaluate(ExpressionUtils.sanitizeExpression(props.functionExpression), { x });
                    return { x, y };
            });
 
            new Chart(ctx, {
                type: 'line',
                data: {
                    datasets: [
                        {
                            label: 'Function',
                            data: Array.from({ length: Math.floor((end - start) / step) + 1 }, (_, i) => {
                                const x = start + i * step;
                                const y = evaluate(ExpressionUtils.sanitizeExpression(props.functionExpression), { x });
                                return { x, y };
                            }),
                            borderColor: 'blue',
                            fill: false,
                        },
                        {
                            label: 'Solution Point',
                            data: [{ x: props.solution, y: evaluate(ExpressionUtils.sanitizeExpression(props.functionExpression), { x: props.solution }) }],
                            borderColor: 'red',
                            backgroundColor: 'red',
                            pointRadius: 10,
                            pointHoverRadius: 8,
                            showLine: false,
                        },
                    ],
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            type: 'linear',
                            position: 'bottom',
                            grid: {
                                color: (context) => context.tick.value === 0 ? 'rgba(0, 0, 0, 1)' : 'rgba(0, 0, 0, 0.1)',
                            },
                        },
                        y: {
                            grid: {
                                color: (context) => context.tick.value === 0 ? 'rgba(0, 0, 0, 1)' : 'rgba(0, 0, 0, 0.1)',
                            },
                            ticks : {
                                callback : function (value) {
                                    return value;
                                },
                            },
                            suggestedMin : Math.min(...data.map(p => p.y)) - 10,
                            suggestedMax : Math.max(...data.map(p => p.y)) + 10,
                        }
                    }
                }
            });
        }
    }
});

const downloadChart = () => {
    if (chartCanvas.value) {
        DownloadChartUtils.downloadSVG(chartCanvas.value, 'function-chart.svg');
    }
};
</script>

<template>
    <div class="card shadow mb-4">
      <div class="card-header py-3 d-flex justify-content-between align-items-center">
        <h6 class="m-0 font-weight-bold text-primary">Graph</h6>
        <button @click="downloadChart" class="btn btn-primary btn-sm">
          Download SVG
        </button>
      </div>
      <div class="card-body">
        <div class="chart-container" ref="chartContainer">
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
    cursor: grab; 
    position: relative;
}

.chart-container:active {
    cursor: grabbing; 
}
</style>