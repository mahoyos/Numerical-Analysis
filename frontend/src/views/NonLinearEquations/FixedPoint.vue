<script setup lang='ts'>
import { ref } from 'vue';
import NonLinearEquationsService from '../../services/NonLinearEquationsService';
import BreadCrumb from '../../components/BreadCrumb.vue';
import Table from '../../components/DataTable.vue';
import Chart from '../../components/ChartSolution.vue';

let breadCrumbList = [
  { title: 'Home', route: '/' },
  { title: 'Non-Linear Equations', route: 'non-linear-equations' },
  { title: 'Fixed Point', route: 'fixed-point' },
];

let tableData = ref([]);

const solutionPoint = ref<number | null>(null);

let chartData = ref({
  function_expression: '',
  solution: 0
});

const handleSubmit = async (event: any) => {
  event.preventDefault();
  let formData = new FormData(event.target);
  const data = {
    initial_guess: parseFloat(formData.get('initialGuess') as string),
    tolerance: parseFloat(formData.get('tolerance') as string),
    max_iterations: parseInt(formData.get('maxIterations') as string, 10),
    function_expression: formData.get('functionExpression') as string,
    g_expression: formData.get('gExpression') as string,
  };

  try {
    const response = await NonLinearEquationsService.postFixedPointData(data);
    tableData.value = response.iterations.map((iteration: any) => ({
      iteration: iteration[0],
      value1: iteration[1],
      value2: iteration[2],
      value3: iteration[3],
    }));
    solutionPoint.value = response.root;
    chartData.value = {
      function_expression: data.function_expression,
      solution: response.root
    };
  } catch (error) {
    console.error('Error posting form data:', error);
  }
};

</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Form</h6>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <div class="row">
          <div class="col">
            <label for="initialGuess">Initial Guess</label>
            <input type="number" class="form-control" id="initialGuess" name="initialGuess" placeholder="Enter initial guess">
          </div>
          <div class="col">
            <label for="tolerance">Tolerance</label>
            <input type="number" class="form-control" id="tolerance" name="tolerance" placeholder="Enter tolerance" step="0.0001">
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="maxIterations">Max Iterations</label>
            <input type="number" class="form-control" id="maxIterations" name="maxIterations" placeholder="Enter max iterations">
          </div>
          <div class="col">
            <label for="functionExpression">Function Expression</label>
            <input type="text" class="form-control" id="functionExpression" name="functionExpression" placeholder="Enter function expression">
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="gExpression">G Expression</label>
            <input type="text" class="form-control" id="gExpression" name="gExpression" placeholder="Enter g expression">
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Submit</button>
      </form>
    </div>
  </div>
  <Table :tableData="tableData" />
  <Chart v-if="solutionPoint !== null" :functionExpression="chartData.function_expression" :solution="chartData.solution" />
  </template>
