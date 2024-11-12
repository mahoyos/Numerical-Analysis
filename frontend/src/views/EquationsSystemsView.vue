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
  if (newSize >= 2 && newSize <= 6) {
    initializeMatrixAndVector(Number(newSize));
  }
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

const methods = [
  {
    name: 'Jacobi',
    description: 'An iterative method that solves a system of linear equations by approximating each diagonal element independently.'
  },
  {
    name: 'Gauss-Seidel',
    description: 'An improvement over the Jacobi method that uses updated values as soon as they are available in each iteration.'
  },
  {
    name: 'SOR (Successive Over-Relaxation)',
    description: 'An accelerated version of the Gauss-Seidel method that uses a relaxation factor to improve convergence.'
  }
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <!-- Introduction Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h4 class="m-0 font-weight-bold text-primary">Systems of Linear Equations</h4>
    </div>
    <div class="card-body">
      <p class="lead mb-4">
        This section provides iterative methods for solving systems of linear equations.
        Each method has its own characteristics and convergence properties.
      </p>

      <!-- Methods Cards -->
      <div class="methods-grid">
        <div v-for="method in methods" :key="method.name" class="method-card">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ method.name }}</h5>
              <p class="card-text">{{ method.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>

  <!-- Input Guide Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Input Format Guide</h5>
    </div>
    <div class="card-body">
      <div class="table-responsive">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th width="20%">Input Field</th>
              <th width="80%">Description</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><b>Tolerance</b></td>
              <td>Acceptable error margin for the root approximation.</td>
            </tr>
            <tr>
              <td><b>Error Type</b></td>
              <td>Defines the error calculation method (absolute or relative).</td>
            </tr>
            <tr>
              <td><b>Max Iterations</b></td>
              <td>Maximum number of iterations allowed to find the solution.</td>
            </tr>
            <tr>
              <td><b>Matrix Size</b></td>
              <td>The number of equations and unknowns in the system (n×n).</td>
            </tr>
            <tr>
              <td><b>Matrix</b></td>
              <td>The n×n coefficient matrix with n rows and n columns.</td>
            </tr>
            <tr>
              <td><b>Solution Vector</b></td>
              <td>An n-dimensional vector holding the constant terms of the equations.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- Calculator Form Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">System Solver Calculator</h5>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <!-- Method Selection -->
        <div class="row mb-4">
          <div class="col-md-6">
            <label class="form-label font-weight-bold" for="methodSelect">Method:</label>
            <select id="methodSelect" v-model="selectedMethod" class="form-control form-select">
              <option value="jacobi">Jacobi</option>
              <option value="gauss-seidel">Gauss-Seidel</option>
              <option value="sor">SOR</option>
            </select>
          </div>

          <div class="col-md-6" v-if="selectedMethod === 'sor'">
            <label class="form-label font-weight-bold" for="omega">Omega:</label>
            <input type="number" class="form-control" id="omega" name="omega" 
                   placeholder="Enter omega value" step="any">
          </div>
        </div>

        <!-- Parameters -->
        <div class="row mb-4">
          <div class="col-md-4">
            <label class="form-label font-weight-bold" for="maxIterations">Max Iterations:</label>
            <input type="number" class="form-control" id="maxIterations" name="maxIterations" 
                   placeholder="Enter max iterations" step="1" min="1" required>
          </div>
          <div class="col-md-4">
            <label class="form-label font-weight-bold" for="tolerance">Tolerance:</label>
            <input type="number" class="form-control" id="tolerance" name="tolerance" 
                   placeholder="Enter tolerance" step="any" min="0.0000001" required>
          </div>
          <div class="col-md-4">
            <label class="form-label font-weight-bold" for="errorType">Error Type:</label>
            <select class="form-control form-select" id="errorType" name="errorType">
              <option value="absolute">Absolute Error</option>
              <option value="relative">Relative Error</option>
            </select>
          </div>
        </div>

        <!-- Matrix Size -->
        <div class="row mb-4">
          <div class="col-md-6">
            <label class="form-label font-weight-bold" for="matrixSize">Matrix Size:</label>
            <input type="number" id="matrixSize" v-model="matrixSize" 
                   class="form-control" :min="2" :max="6" required>
          </div>
        </div>

        <!-- Matrix and Vectors -->
        <div class="row mb-4">
          <div class="col-md-4">
            <label class="form-label font-weight-bold">Matrix ({{ matrixSize }}×{{ matrixSize }}):</label>
            <div class="matrix-inputs">
              <div v-for="(row, rowIndex) in matrixValues" :key="'row-' + rowIndex" 
                   class="d-flex gap-2 mb-2">
                <input v-for="(value, colIndex) in row" 
                       :key="'col-' + colIndex"
                       v-model.number="matrixValues[rowIndex][colIndex]"
                       type="number" step="any" class="form-control"
                       :placeholder="`a${rowIndex+1}${colIndex+1}`">
              </div>
            </div>
          </div>

          <div class="col-md-4">
            <label class="form-label font-weight-bold">Solution Vector:</label>
            <div class="vector-inputs">
              <input v-for="index in matrixSize" 
                     :key="'sol-' + index"
                     v-model.number="solutionVector[index - 1]"
                     type="number" step="any" class="form-control mb-2"
                     :placeholder="`b${index}`">
            </div>
          </div>

          <div class="col-md-4" v-if="selectedMethod === 'sor'">
            <label class="form-label font-weight-bold">Initial Guess Vector:</label>
            <div class="vector-inputs">
              <input v-for="index in matrixSize"
                     :key="'guess-' + index"
                     v-model.number="initialGuess[index - 1]"
                     type="number" step="any" class="form-control mb-2"
                     :placeholder="`x${index}`">
            </div>
          </div>
        </div>

        <!-- Submit Button -->
        <div class="text-end">
          <button type="submit" class="btn btn-primary">
            Solve System
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Results -->
  <div v-if="tableData.length > 0" class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Solution Results</h5>
    </div>
    <div class="card-body">
      <Table :tableData="tableData" />
      <LineGraph v-if="matrixSize === 2"
                :matrixValues="matrixValues"
                :solutionVector="solutionVector"
                :matrixSize="matrixSize" />
    </div>
  </div>
</template>

<style scoped></style>
