<script setup lang='ts'>
import { ref } from 'vue';
import NonLinearEquationsService from '../../services/NonLinearEquationsService';
import BreadCrumb from '../../components/BreadCrumb.vue';
import Table from '../../components/DataTable.vue';
import Chart from '../../components/ChartSolution.vue';

let breadCrumbList = [
  { title: 'Home', route: '/' },
  { title: 'Non-Linear Equations', route: 'non-linear-equations' },
  { title: 'False Position', route: 'false-position' },
];

let tableData = ref([]);
const solutionPoint = ref<number | null>(null);
const chartData = ref({
  function_expression: '',
  solution: 0
});

const message = ref('');
const messageType = ref<number | null>(null);

const handleSubmit = async (event: any) => {
  event.preventDefault();
  let formData = new FormData(event.target);
  const data = {
    left_bound: parseFloat(formData.get('leftBound') as string),
    right_bound: parseFloat(formData.get('rightBound') as string),
    tolerance: parseFloat(formData.get('tolerance') as string),
    max_iterations: parseInt(formData.get('maxIterations') as string, 10),
    function_expression: formData.get('functionExpression') as string,
  };

  try {
    const response = await NonLinearEquationsService.postFalsePositionData(data);
    
    messageType.value = response.message_type;
    message.value = response.message;

    if (response.message_type === 1) {
      if (response.iterations && Array.isArray(response.iterations)) {
        tableData.value = response.iterations.map((iteration: any) => ({
          iteration: iteration[0],
          value1: iteration[1],
          value2: iteration[2],
          value3: iteration[3],
        }));
      }

      if (response.root !== undefined) {
        solutionPoint.value = response.root;
        chartData.value = {
          function_expression: data.function_expression,
          solution: response.root
        };
      }
    } else {
      tableData.value = [];
      solutionPoint.value = null;
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
      <h6 class="m-0 font-weight-bold text-primary">False Position Form</h6>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <div class="row">
          <div class="col">
            <label for="lowerBound">Left Bound</label>
            <input type="number" class="form-control" id="leftBound" name="leftBound" placeholder="Enter left bound">
          </div>
          <div class="col">
            <label for="rightBound">Right Bound</label>
            <input type="number" class="form-control" id="rightBound" name="rightBound" placeholder="Enter right bound">
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="tolerance">Tolerance</label>
            <input type="number" class="form-control" id="tolerance" name="tolerance" placeholder="Enter tolerance" step="0.0001">
          </div>
          <div class="col">
            <label for="maxIterations">Max Iterations</label>
            <input type="number" class="form-control" id="maxIterations" name="maxIterations" placeholder="Enter max iterations">
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="functionExpression">Function Expression</label>
            <input type="text" class="form-control" id="functionExpression" name="functionExpression" placeholder="Enter function expression">
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-3">Submit</button>
      </form>
    </div>
  </div>

  <div v-if="message" class="alert" :class="{'alert-success': messageType === 1, 'alert-danger': messageType === 0}">
    {{ message }}
  </div>

  <Table v-if="messageType === 1" :tableData="tableData" />
  <Chart v-if="solutionPoint !== null && messageType === 1" :functionExpression="chartData.function_expression" :solution="chartData.solution" />
</template>
