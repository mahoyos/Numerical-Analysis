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
const messageText = ref<string>('');
const success = ref<boolean>(false);
const finalSolution = ref<number[]>([]);
const spectralRadius = ref<number | null>(null);

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
  
  // Reset states
  messageType.value = null;
  messageText.value = '';
  success.value = false;
  tableData.value = [];
  finalSolution.value = [];
  spectralRadius.value = null;

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
    
    if (response.status === 'error') {
      messageType.value = 'error';
      
      // Customize message based on error code
      if (response.error.code === 'CONVERGENCE_ERROR') {
        let methodRequirements = '';
        switch (selectedMethod.value) {
          case 'jacobi':
            methodRequirements = 'The Jacobi method requires the matrix to be strictly diagonally dominant to guarantee convergence.';
            break;
          case 'gauss-seidel':
            methodRequirements = 'The Gauss-Seidel method requires the matrix to be either strictly diagonally dominant or symmetric positive definite.';
            break;
          case 'sor':
            methodRequirements = 'The SOR method requires an appropriate choice of ω parameter and the matrix to be symmetric positive definite.';
            break;
        }
        
        messageText.value = `Error: The method failed to converge to a valid solution.\n\n` +
                          `${methodRequirements}\n\n` +
                          `Suggestions:\n` +
                          `• Verify that your matrix meets the method's requirements\n` +
                          `• Try increasing the maximum number of iterations\n` +
                          `• Consider using a less strict tolerance value\n` +
                          `• Try a different method`;
      } else {
        messageText.value = `Error Code: ${response.error.code}\n${response.error.message}`;
      }
      return;
    }

    success.value = true;
    tableData.value = response.iterations.map((iteration: any) => ({
      iteration: iteration[0],
      values: iteration[1],
      error: iteration[2],
    }));
    
    finalSolution.value = response.root;
    spectralRadius.value = response.spectral_radius;

  } catch (error: any) {
    messageType.value = 'error';
    messageText.value = 'Error Code: UNKNOWN_ERROR\nAn unexpected error occurred while processing your request';
    console.error('Error posting form data:', error);
  }
};

const methods = [
  {
    name: 'Jacobi',
    description: 'An iterative method that solves a system of linear equations by computing each variable using previous iteration values. All variables are updated simultaneously after each iteration.'
  },
  {
    name: 'Gauss-Seidel',
    description: 'An iterative method that improves upon Jacobi by using the most recently calculated values within the same iteration, typically resulting in faster convergence.'
  },
  {
    name: 'SOR (Successive Over-Relaxation)',
    description: 'An accelerated version of Gauss-Seidel that introduces a relaxation factor (ω) to speed up convergence. When 0 < ω < 1 it becomes under-relaxation, and when 1 < ω < 2 it becomes over-relaxation.'
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

  <!-- Methods Comparison Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Methods Comparison</h5>
    </div>
    <div class="card-body">
      <p class="mb-4">
        Each iterative method has its own convergence properties and requirements. Understanding these is crucial for solving systems of linear equations effectively.
      </p>
      <div class="table-responsive">
        <table class="table table-bordered">
          <thead>
            <tr>
              <th>Method</th>
              <th>Diagonally Dominant Required</th>
              <th>Positive Definite Required</th>
              <th>Key Characteristics</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Jacobi</td>
              <td>Yes</td>
              <td>Not necessarily</td>
              <td>
                <ul class="mb-0">
                  <li>Simple implementation and concept</li>
                  <li>Parallel-friendly as all updates are independent</li>
                  <li>Generally slower convergence rate</li>
                  <li>Requires storage of previous iteration values</li>
                  <li>Guaranteed to converge for strictly diagonally dominant matrices</li>
                </ul>
              </td>
            </tr>
            <tr>
              <td>Gauss-Seidel</td>
              <td>Yes</td>
              <td>Not necessarily</td>
              <td>
                <ul class="mb-0">
                  <li>Usually converges in fewer iterations than Jacobi</li>
                  <li>Uses less memory as it updates values in place</li>
                  <li>Sequential nature makes parallelization difficult</li>
                  <li>Guaranteed to converge for strictly diagonally dominant or symmetric positive definite matrices</li>
                </ul>
              </td>
            </tr>
            <tr>
              <td>SOR</td>
              <td>Not necessarily</td>
              <td>Yes</td>
              <td>
                <ul class="mb-0">
                  <li>Can achieve fastest convergence of all three methods</li>
                  <li>Optimal ω depends on matrix properties</li>
                  <li>For ω = 1, reduces to Gauss-Seidel</li>
                  <li>Typically 1 < ω < 2 for over-relaxation</li>
                  <li>Convergence highly dependent on choice of ω</li>
                </ul>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="mt-4">
        <h6 class="font-weight-bold">Important Notes:</h6>
        <ul>
          <li><strong>Diagonally Dominant:</strong> A matrix is strictly diagonally dominant if |aii| > Σ|aij| (i≠j) for each row i, where aii is the diagonal element.</li>
          <li><strong>Positive Definite:</strong> A symmetric matrix A is positive definite if xᵀAx > 0 for all non-zero vectors x. This property ensures unique solutions and convergence.</li>
          <li><strong>Convergence Speed:</strong> Generally, with optimal parameters: SOR > Gauss-Seidel > Jacobi.</li>
          <li><strong>Method Selection:</strong> Consider matrix properties, system size, and computational resources when choosing a method.</li>
          <li><strong>Iteration Cost:</strong> Each method has different per-iteration computational costs, which should be considered alongside convergence rate.</li>
        </ul>
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

          <div class="col-md-4">
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

  <!-- Error Message -->
  <div v-if="messageType === 'error'" class="alert alert-danger mb-4" role="alert">
    <i class="fas fa-exclamation-circle me-2"></i>
    <div style="white-space: pre-line">{{ messageText }}</div>
  </div>

  <!-- Results -->
  <div v-if="success && tableData.length > 0" class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Solution Results</h5>
    </div>
    <div class="card-body">
      <!-- Final Solution -->
      <div class="mb-4">
        <h6 class="font-weight-bold">Final Solution:</h6>
        <div class="d-flex gap-3">
          <div v-for="(value, index) in finalSolution" :key="index" class="text-primary">
            x{{ index + 1 }} = {{ value.toFixed(6) }}
          </div>
        </div>
      </div>

      <!-- Spectral Radius -->
      <div v-if="spectralRadius !== null" class="mb-4">
        <h6 class="font-weight-bold">Spectral Radius:</h6>
        <div class="text-primary">
          ρ = {{ spectralRadius.toFixed(6) }}
          <span class="ms-2 text-muted">
            ({{ spectralRadius < 1 ? 'Method converges' : 'Method could not converge' }})
          </span>
        </div>
      </div>

      <!-- Iteration Table -->
      <Table :tableData="tableData" />
      
      <!-- Line Graph (only for 2x2 systems) -->
      <LineGraph v-if="matrixSize === 2"
                :matrixValues="matrixValues"
                :solutionVector="solutionVector"
                :matrixSize="matrixSize" />
    </div>
  </div>
</template>

<style scoped></style>
