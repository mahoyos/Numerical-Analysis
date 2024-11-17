<script setup lang="ts">
import { ref, watch } from 'vue';
import BreadCrumb from '../components/BreadCrumb.vue';
import InterpolationsService from '../services/InterpolationsService';
import InterpolationGraph from '../components/InterpolationGraph.vue';

let breadCrumbList = [
  {
    title: 'Home', route: '/',
  },
  {
    title: 'Interpolations', route: 'interpolations' 
  },
];

const selectedMethod = ref('newton'); 
const degree = ref<number | null>(null);
const matrixSize = ref(2);
const xVector = ref<number[]>([]);
const yVector = ref<number[]>([]);
const response = ref<any>(null);
const errorMessage = ref('');

const initializeMatrixAndVector = (size: number) => {
  xVector.value = Array(size).fill(0);
  yVector.value = Array(size).fill(0);
};

watch(matrixSize, (newSize) => {
  initializeMatrixAndVector(Number(newSize));
});

initializeMatrixAndVector(matrixSize.value);

const hasRepeatedXValues = (xValues: number[]): boolean => {
  const uniqueValues = new Set(xValues);
  return uniqueValues.size !== xValues.length;
};

const handleSubmit = async (event: Event) => {
  event.preventDefault();
  errorMessage.value = '';

  if (hasRepeatedXValues(xVector.value)) {
    errorMessage.value = 'X values must be unique. Please check for repeated values.';
    return;
  }

  if (selectedMethod.value === 'spline' && (!degree.value || ![1, 2].includes(degree.value))) {
    errorMessage.value = 'For spline interpolation, degree must be either 1 or 2.';
    return;
  }

  const data: any = {
    method: selectedMethod.value,
    x_points: xVector.value,
    y_points: yVector.value,
  };

  if (selectedMethod.value === 'spline' && degree.value !== null) {
    data.degree = degree.value;
  }

  try {
    response.value = await InterpolationsService.postInterpolationsData(data);
  } catch (error) {
    console.log('Error posting form data:', error);
  }
};

const methods = [
  {
    name: 'Newton',
    description: 'Uses divided differences to construct an interpolating polynomial that passes through all given points.'
  },
  {
    name: 'Lagrange',
    description: 'Constructs polynomials using a linear combination of basis polynomials to interpolate given points.'
  },
  {
    name: 'Spline',
    description: 'Creates piecewise polynomial functions that interpolate points with smooth transitions between segments.'
  },
  {
    name: 'Vandermonde',
    description: 'Uses a matrix-based approach to find coefficients of the interpolating polynomial.'
  }
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <!-- Introduction Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h4 class="m-0 font-weight-bold text-primary">Interpolation Methods</h4>
    </div>
    <div class="card-body">
      <p class="lead mb-4">
        This section provides various numerical methods for interpolating data points.
        Each method constructs a function that passes through given points, with different characteristics and applications.
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

  <!-- Input Format Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Input Format Guide</h5>
    </div>
    <div class="card-body">
      <p class="mb-4">
        To use the interpolation methods, you'll need to provide the following inputs:
      </p>
      
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
              <td><b>Number (n)</b></td>
              <td>Represents the number of (𝑥,𝑦) data points to be provided for interpolation.</td>
            </tr>
            <tr>
              <td><b>Error Type</b></td>
              <td>Defines the error calculation method (absolute or relative).</td>
            </tr>
            <tr>
              <td><b>X Vector</b></td>
              <td>Contains the 𝑥ᵢ points where the function values are known. These are the independent values that serve as reference points for building the interpolating function.</td>
            </tr>
            <tr>
              <td><b>Y Vector</b></td>
              <td>Contains the 𝑦ᵢ values corresponding to each 𝑥ᵢ point. These are the dependent function values to be interpolated.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="alert alert-info mt-3">
        <i class="fas fa-info-circle me-2"></i>
        Note: For spline interpolation, you'll need to specify the degree (1 or 2) of the piecewise polynomial functions.
      </div>
    </div>
  </div>

  <!-- Form Card -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Interpolation Calculator</h5>
    </div>
    <div class="card-body">
      <form @submit="handleSubmit">
        <!-- Method Selection -->
        <div class="row mb-4">
          <div class="col-md-6">
            <label class="form-label font-weight-bold" for="methodSelect">Method:</label>
            <select 
              id="methodSelect" 
              v-model="selectedMethod" 
              class="form-control form-select"
            >
              <option value="newton">Newton</option>
              <option value="lagrange">Lagrange</option>
              <option value="spline">Spline</option>
              <option value="vandermonde">Vandermonde</option>
            </select>
          </div>

          <div class="col-md-6" v-if="selectedMethod === 'spline'">
            <label class="form-label font-weight-bold" for="degree">Degree:</label>
            <input 
              type="number" 
              id="degree" 
              v-model="degree" 
              class="form-control" 
              :min="1"
              :max="2"
              placeholder="Enter degree (1 or 2)" 
            />
          </div>
        </div>

        
          <div class="col-md-6">
            <label class="form-label font-weight-bold" for="matrixSize">Number of points (n):</label>
            <input 
              type="number" 
              id="matrixSize" 
              v-model="matrixSize" 
              class="form-control" 
              :min="2" 
              step="1"
              placeholder="Enter number of points" 
            />
          </div>
        

        <!-- Vectors Input -->
        <div class="row mb-4">
          <div class="col-md-6">
            <label class="form-label font-weight-bold">X Vector:</label>
            <div class="vector-inputs">
              <input 
                v-for="index in matrixSize" 
                :key="'x-' + index" 
                v-model.number="xVector[index - 1]"
                type="number" 
                step="any"
                class="form-control mb-2" 
                :placeholder="'x' + index"
              />
            </div>
          </div>

          <div class="col-md-6">
            <label class="form-label font-weight-bold">Y Vector:</label>
            <div class="vector-inputs">
              <input 
                v-for="index in matrixSize" 
                :key="'y-' + index" 
                v-model.number="yVector[index - 1]"
                type="number" 
                step="any"
                class="form-control mb-2" 
                :placeholder="'y' + index"
              />
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="errorMessage" class="alert alert-danger mb-4">
          <i class="fas fa-exclamation-circle me-2"></i>
          {{ errorMessage }}
        </div>

        <!-- Submit Button -->
        <div class="text-end">
          <button type="submit" class="btn btn-primary">
            Calculate Interpolation
          </button>
        </div>
      </form>
    </div>
  </div>

  <!-- Result Graph -->
  <div v-if="response" class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">Interpolation Result</h5>
    </div>
    <div class="card-body">
      <InterpolationGraph 
        :polynom="response.polynom" 
        :method="selectedMethod"
        :xPoints="xVector"
        :yPoints="yVector"
      />
    </div>
  </div>
</template>

<style scoped>
.card-text {
  margin-bottom: 1rem;
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  padding: 0.75rem;
}

.method-card {
  width: 100%;
}

.form-control {
  margin-bottom: 1rem;
}

code {
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
}

@media (max-width: 768px) {
  .methods-grid {
    grid-template-columns: 1fr;
  }
}

.form-label {
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.vector-inputs {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}
</style>
