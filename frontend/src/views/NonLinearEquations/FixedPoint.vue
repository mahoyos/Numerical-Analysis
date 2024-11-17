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

const message = ref('');
const messageType = ref<string | null>(null);

const handleSubmit = async (event: any) => {
  event.preventDefault();
  let formData = new FormData(event.target);
  const data = {
    initial_guess: parseFloat(formData.get('initialGuess') as string),
    tolerance: parseFloat(formData.get('tolerance') as string),
    max_iterations: parseInt(formData.get('maxIterations') as string, 10),
    function_expression: formData.get('functionExpression') as string,
    g_expression: formData.get('gExpression') as string,
    error_type : formData.get('errorType') as string,
  };

  try {
    const response = await NonLinearEquationsService.postFixedPointData(data);

    messageType.value = response.status;
    message.value = response.error.message;

    if(response.status === 'success'){
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
    }
  } catch (error) {
    console.error('Error posting form data:', error);
  }
};

</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />


  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Fixed Point Method Form Input</h6>
    </div>
    <div class="card-body">
      <ul>
        <li class="mt-3"><b>Initial Guess: </b>Starting value for the iteration to approximate the root.</li>
        <li class="mt-3"><b>Tolerance: </b>Acceptable error margin for the root approximation.</li>
        <li class="mt-3"><b>Error Type: </b>Defines the error calculation method (e.g., absolute or relative).</li>
        <li class="mt-3"><b>Max Iterations: </b>Maximum number of iterations allowed to find the root.</li>
        <li class="mt-3"><b>Function Expression: </b>The mathematical function where the root is being sought, written in Python syntax (e.g., `**` for powers) without quotes.</li>
        <li class="mt-3"><b>G Expression: </b>The transformation function 𝑔(𝑥) used to iterate towards the fixed point, written in Python syntax (e.g., `**` for powers) without quotes.</li>
      </ul>
    </div>
    
  </div>


  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Fixed Point Method Form</h6>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <div class="row">
          <div class="col">
            <label for="initialGuess">Initial Guess</label>
            <input type="number" class="form-control" id="initialGuess" name="initialGuess" placeholder="Enter initial guess" step="any">
          </div>
          <div class="col">
            <label for="maxIterations">Max Iterations</label>
            <input type="text" class="form-control" id="maxIterations" name="maxIterations" placeholder="Enter max iterations">
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="tolerance">Tolerance</label>
            <input 
              type="number" 
              class="form-control" 
              id="tolerance" 
              name="tolerance" 
              placeholder="Enter tolerance" 
              step="any" 
              min="0.0000001" 
              required
              oninvalid="this.setCustomValidity('Tolerance must be a positive number.')"
              oninput="this.setCustomValidity('')"
            >
          </div>
          <div class="col">
            <label for="errorType">Error Type</label>
            <select class="form-control" id="errorType" name="errorType">
              <option value="absolute">Absolute Error</option>
              <option value="relative">Relative Error</option>
            </select>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="functionExpression">Function Expression</label>
            <input type="text" class="form-control" id="functionExpression" name="functionExpression" placeholder="Enter function expression" />
          </div>
          <div class="col">
            <label for="gExpression">G Expression</label>
            <input type="text" class="form-control" id="gExpression" name="gExpression" placeholder="Enter g expression"/>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Submit</button>
      </form>
    </div>
  </div>
  <div v-if="message" class="alert" :class="{'alert-success': messageType === 'success', 'alert-danger': messageType === 'error'}">
    {{ message }}
  </div>
  <div v-if="solutionPoint !== null" class="alert alert-info">
    <strong>Root found:</strong> {{ solutionPoint }}
  </div>
  <Table v-if="messageType === 'success'" :tableData="tableData" />
  <Chart v-if="solutionPoint !== null" :functionExpression="chartData.function_expression" :solution="chartData.solution" />
  </template>
