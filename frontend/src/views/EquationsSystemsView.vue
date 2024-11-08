<script setup lang="ts">
import { ref, watch } from 'vue';
import BreadCrumb from '../components/BreadCrumb.vue';
import SystemsEquationsService from '../services/SystemsEquationsService';
import Table from '../components/SystemsEquationsDataTable.vue';
import LineGraph from '../components/LineGraph.vue';

let breadCrumbList = [
  {
    title: 'Home', route: '/',
  },
  {
    title: 'Equations Systems', route: 'equations-systems' 
  },
];

const selectedMethod = ref('jacobi'); 
const matrixSize = ref(2);
const matrixValues = ref<number[][]>([]);
const solutionVector = ref<number[]>([]);
const initialGuess = ref<number[]>([]);

const messageType = ref<string | null>(null);

let tableData = ref([]);

const initializeMatrixAndVector = (size: number) => {
  matrixValues.value = Array.from({ length: size }, () => Array(size).fill(0));
  solutionVector.value = Array(size).fill(0);
  initialGuess.value = Array(size).fill(0);
};

watch(matrixSize, (newSize) => {
  initializeMatrixAndVector(Number(newSize));
});

initializeMatrixAndVector(matrixSize.value);

const handleSubmit = async (event : Event) => {
  event.preventDefault();

  let formData = new FormData(event.target as HTMLFormElement);
  const data = {
    matrix_A: matrixValues.value,
    solution_vector: solutionVector.value,
    initial_guess: initialGuess.value,
    omega: parseFloat(formData.get('omega') as string),
    tolerance: parseFloat(formData.get('tolerance') as string),
    max_iterations: parseInt(formData.get('maxIterations') as string, 10),
    error_type: formData.get('errorType') as string,
    method : selectedMethod.value,
  };

  try {
    const response = await SystemsEquationsService.postSystemsEquationsData(data);
    
    tableData.value = response.iteration_data.map((iteration: any) => ({
      iteration: iteration[0],
      values: iteration[1],
      error: iteration[2],
    }));

  } catch (error) {
    console.log('Error posting form data:', error);
  }
};
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Equations System Form Input</h6>
    </div>
    <div class="card-body">
      <ul>

        <li class="mt-3"><b>Tolerance: </b>Acceptable error margin for the root approximation.</li>
        <li class="mt-3"><b>Error Type: </b>Defines the error calculation method (e.g., absolute or relative).</li>
        <li class="mt-3"><b>Max Iterations: </b>Maximum number of iterations allowed to find the root.</li>
        <li class="mt-3"><b>Matrix Size: </b>The number of equations and unknowns in the system.</li>
        <li class="mt-3"><b>Matrix (nxn): </b>The 𝑛×𝑛 matrix is a square matrix with 𝑛 rows and 𝑛 columns, intended to store specific values related to the problem</li>
        <li class="mt-3"><b>Solution Vector: </b>Is an 𝑛-dimensional vector that holds the solution values associated with each row or column in the 𝑛×𝑛 matrix, representing outcomes from calculations or optimizations based on the matrix data.</li>
      </ul>
    </div>

    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Equations Systems</h6>
    </div>
    <form  @submit="handleSubmit" class="p-4">
      <div class="form-group">
        <label for="methodSelect">Choose a method:</label>
        <select id="methodSelect" v-model="selectedMethod" class="form-control">
          <option value="jacobi">Jacobi</option>
          <option value="gauss-seidel">Gauss-Seidel</option>
          <option value="sor">SOR</option>
        </select>
      </div>
      <div class="row mt-3">
          <div class="col" v-if="selectedMethod === 'sor'">
            <label for="omega">Omega</label>
            <input type="text" class="form-control" id="omega" name="omega" placeholder="Enter omega value">
          </div>
          <div class="col">
            <label for="maxIterations">Max Iterations</label>
            <input type="number" class="form-control" id="maxIterations" name="maxIterations" placeholder="Enter max iterations" required>
          </div>
        </div>
        <div class="row mt-3">
          <div class="col">
            <label for="tolerance">Tolerance</label>
            <input type="number" class="form-control" id="tolerance" name="tolerance" placeholder="Enter tolerance" step="0.0001" required>
          </div>
          <div class="col">
            <label for="errorType">Error Type</label>
            <select class="form-control" id="errorType" name="errorType">
              <option value="absolute">Absolute Error</option>
              <option value="relative">Relative Error</option>
            </select>
          </div>
        </div>
      <div v-if="selectedMethod" class="form-group mt-3">
        <label for="matrixSize">Matrix size:</label>
        <input 
          type="number" 
          id="matrixSize" 
          v-model="matrixSize" 
          class="form-control" 
          :min="2" 
          placeholder="Enter matrix size" 
        />
      </div>
      

      <div class="row mt-3">
        <div class="col">
          <div v-if="matrixSize" class="mt-3">
            <label>Enter the matrix :  {{ matrixSize }}x{{ matrixSize }}</label>
            <div class="d-flex flex-column mb-2">
              <div v-for="(row, rowIndex) in matrixValues" :key="'row-' + rowIndex" class="d-flex mb-2">
                <input 
                  v-for="(value, colIndex) in row" 
                  :key="'col-' + colIndex" 
                  v-model.number="matrixValues[rowIndex][colIndex]" 
                  type="number" 
                  class="form-control mx-1" 
                  style="width: 70px;"
                />
              </div>
            </div>
          </div>
        </div>

        <div class="col">
          <div v-if="matrixSize" class="mt-3">
            <label>Enter the solution vector :</label>
            <div class="d-flex flex-column mb-2">
              <input 
                v-for="index in matrixSize" 
                :key="'sol-' + index" 
                v-model.number="solutionVector[index - 1]" 
                type="number" 
                step="any"
                class="form-control mx-1 mb-2" 
                style="width: 70px;"
              />
            </div>
          </div>
        </div>

        <div class="col" v-if="selectedMethod === 'sor'">
          <div v-if="matrixSize" class="mt-3">
            <label>Enter the initial guess vector :</label>
            <div class="d-flex flex-column mb-2">
              <input 
                v-for="index in matrixSize" 
                :key="'sol-' + index" 
                v-model.number="initialGuess[index - 1]" 
                type="number" 
                class="form-control mx-1 mb-2" 
                style="width: 70px;"
              />
            </div>
          </div>
        </div>
      </div>
      
      <button type="submit" class="btn btn-primary mt-3">Submit</button>
    </form>
  </div>
  <Table :tableData="tableData" />
  <LineGraph 
    v-if="matrixSize === 2" 
    :matrixValues="matrixValues" 
    :solutionVector="solutionVector" 
    :matrixSize="matrixSize" 
  />
</template>

<style scoped></style>
