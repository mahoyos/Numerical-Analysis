<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Chart, registerables } from 'chart.js';
import { evaluate } from 'mathjs';
import ExpressionUtils from '../util/ChartUtils';

Chart.register(...registerables);

const props = defineProps<{
    functionExpression: string;
    solution: number;
}>();

const chartCanvas = ref<HTMLCanvasElement | null>(null);

onMounted(() => {
    if (chartCanvas.value) {
        const ctx = chartCanvas.value.getContext('2d');
        if (ctx) {
            const range = 20;
            const start = props.solution - range;
            const end = props.solution + range;

            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: Array.from({ length: end - start + 1 }, (_, i) => start + i),
                    datasets: [
                        {
                            label: 'Function',
                            data: Array.from({ length: end - start + 1 }, (_, i) => {
                                const x = start + i;
                                const result = evaluate(ExpressionUtils.sanitizeExpression(props.functionExpression), { x });
                                return result;
                            }),
                            borderColor: 'blue',
                            fill: false,
                        },
                        {
                            label: 'Solution Point',
                            data: Array.from({ length: end - start + 1 }, (_, i) => {
                                const x = start + i;
                                return x === props.solution ? evaluate(ExpressionUtils.sanitizeExpression(props.functionExpression), { x }) : null;
                            }),
                            borderColor: 'red',
                            pointRadius: 10,
                            pointBackgroundColor: 'red',
                            showLine: false,
                        },
                    ],
                },
                options: {
                    scales: {
                        x: {
                            grid: {
                                color: (context) => {
                                    if (context.tick.value === 0) {
                                        return 'rgba(0, 0, 0, 1)';
                                    }
                                    return 'rgba(0, 0, 0, 0.1)';
                                }
                            }
                        },
                        y: {
                            grid: {
                                color: (context) => {
                                    if (context.tick.value === 0) {
                                        return 'rgba(0, 0, 0, 1)';
                                    }
                                    return 'rgba(0, 0, 0, 0.1)';
                                }
                            },
                        }
                    }
                }
            });
        }
    }
});
</script>

<template>
    <div class="card shadow mb-4">
      <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Graph</h6>
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