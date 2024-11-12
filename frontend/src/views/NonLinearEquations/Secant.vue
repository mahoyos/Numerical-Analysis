<script setup lang='ts'>
import { ref } from 'vue';
import NonLinearEquationsService from '../../services/NonLinearEquationsService';
import BreadCrumb from '../../components/BreadCrumb.vue';
import Table from '../../components/DataTable.vue';
import Chart from '../../components/ChartSolution.vue';

let breadCrumbList = [
  { title: 'Home', route: '/' },
  { title: 'Non-Linear Equations', route: 'non-linear-equations' },
  { title: 'Secant', route: 'secant' },
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
  const leftBound = parseFloat(formData.get('leftBound') as string);
  const rightBound = parseFloat(formData.get('rightBound') as string);

  if (leftBound >= rightBound) {
    messageType.value = 'error';
    message.value = 'Left Bound must be less than Right Bound.';
    return;
  }

  const data = {
    left_bound: leftBound,
    right_bound: rightBound,
    tolerance: parseFloat(formData.get('tolerance') as string),
    max_iterations: parseInt(formData.get('maxIterations') as string, 10),
    function_expression: formData.get('functionExpression') as string,
    error_type : formData.get('errorType') as string,
  };

  try {
    const response = await NonLinearEquationsService.postSecantData(data);
    
    messageType.value = response.status;
    message.value = response.error?.message || response.message ;
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
    messageType.value = 'error';
    message.value = 'An error occurred while processing your request';
  }
};
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Secant Method Form Input</h6>
    </div>
    <div class="card-body">
      <ul>
        <li class="mt-3"><b>Left Bound: </b>Starting point on the left side of the interval for the root search.</li>
        <li class="mt-3"><b>Right Bound: </b>Starting point on the right side of the interval for the root search.</li>
        <li class="mt-3"><b>Tolerance: </b>Acceptable error margin for the root approximation.</li>
        <li class="mt-3"><b>Error Type: </b>Defines the error calculation method (e.g., absolute or relative).</li>
        <li class="mt-3"><b>Max Iterations: </b>Maximum number of iterations allowed to find the root.</li>
        <li class="mt-3"><b>Function Expression: </b>The mathematical function where the root is being sought, written in Python syntax (e.g., `**` for powers) without quotes.</li>
      </ul>
    </div>
    
  </div>

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Secant Method Form</h6>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <div class="row">
          <div class="col">
            <label >Left Bound</label>
            <input type="number" class="form-control" id="leftBound" name="leftBound" placeholder="Enter left bound" step="any" required>
          </div>
          <div class="col">
            <label for="rightBound">Right Bound</label>
            <input type="number" class="form-control" id="rightBound" name="rightBound" placeholder="Enter right bound" step="any" required>
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
            <label for="maxIterations">Max Iterations</label>
            <input type="number" class="form-control" id="maxIterations" name="maxIterations" placeholder="Enter max iterations" required min="1" step="1" oninvalid="this.setCustomValidity('Max Iterations must be a positive integer greater than zero.')" oninput="this.setCustomValidity('')">
          </div>
          <div class="col">
            <label for="functionExpression">Function Expression</label>
            <input type="text" class="form-control" id="functionExpression" name="functionExpression" placeholder="Enter function expression" required>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Submit</button>
      </form>
    </div>
  </div>
  <div v-if="message" class="alert" :class="{'alert-success': messageType === 'success', 'alert-danger': messageType === 'error'}">
    {{ message }}
  </div>
  <Table v-if="messageType === 'success'" :tableData="tableData" />
  <Chart v-if="solutionPoint !== null" :functionExpression="chartData.function_expression" :solution="chartData.solution" />
</template>


