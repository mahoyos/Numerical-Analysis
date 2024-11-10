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

  if (selectedMethod.value === 'spline' && degree.value !== null) {
    if (matrixSize.value - degree.value !== 1) {
      errorMessage.value = 'For spline interpolation, n - degree must equal 1';
      return;
    }
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
    //initializeMatrixAndVector(matrixSize.value);
  } catch (error) {
    console.log('Error posting form data:', error);
  }
};
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Interpolations Form Input</h6>
    </div>
    <div class="card-body">
      <ul>
        <li class="mt-3"><b>(n): </b>Represents the number of (𝑥,𝑦) data points to be provided for interpolation.</li>
        <li class="mt-3"><b>Error Type: </b>Defines the error calculation method (e.g., absolute or relative).</li>
        <li class="mt-3"><b>X Vector: </b>This vector contains the 𝑥𝑖 points where the function values are known. These are the independent values that serve as reference points for building the interpolating function or polynomial.</li>
        <li class="mt-3"><b>Y Vector: </b> This vector contains the 𝑦𝑖 values corresponding to each 𝑥𝑖 point. These are the dependent function values that to be interpolate. </li>
      </ul>
    </div>
  </div>

    <div class="card shadow mb-4">
      <div class="card-header py-3">
        <h6 class="m-0 font-weight-bold text-primary">Interpolations</h6>
      </div>
      <form @submit="handleSubmit" class="p-4">
        <div class="form-group">
          <label for="methodSelect">Choose a method:</label>
          <select id="methodSelect" v-model="selectedMethod" class="form-control">
            <option value="newton">Newton</option>
            <option value="lagrange">Lagrange</option>
            <option value="spline">Spline</option>
            <option value="vandermonde">Vandermonde</option>
          </select>
        </div>
        
        <div class="form-group mt-3" v-if="selectedMethod === 'spline'">
          <label for="degree">Enter the degree:</label>
          <input 
            type="number" 
            id="degree" 
            v-model="degree" 
            class="form-control" 
            :min="1" 
            placeholder="Enter the degree" 
          />
        </div>
        
        <div class="row mt-3">
          <div class="col">
            <label for="matrixSize">Enter a number (n):</label>
          <input 
            type="number" 
            id="matrixSize" 
            v-model="matrixSize" 
            class="form-control" 
            :min="2" 
            step="1"
            placeholder="Enter a number" 
            />
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
            <div v-if="matrixSize" class="mt-3">
              <label>Enter X vector:</label>
              <div class="d-flex flex-column mb-2">
                <input 
                  v-for="index in matrixSize" 
                  :key="'vector1-' + index" 
                  v-model.number="xVector[index - 1]"
                  type="number" 
                  step="any"
                  class="form-control mx-1 mb-2" 
                  style="width: 70px;"
                />
              </div>
            </div>
          </div>

          <div class="col">
            <div v-if="matrixSize" class="mt-3">
              <label>Enter Y vector:</label>
              <div class="d-flex flex-column mb-2">
                <input 
                  v-for="index in matrixSize" 
                  :key="'vector2-' + index" 
                  v-model.number="yVector[index - 1]"
                  type="number" 
                  step="any"
                  class="form-control mx-1 mb-2" 
                  style="width: 70px;"
                />
              </div>
            </div>
          </div>
        </div>
        
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>
        <button type="submit" class="btn btn-primary mt-3">Submit</button>
      </form>
    </div>

    <InterpolationGraph 
      v-if="response" 
      :polynom="response.polynom" 
      :method="selectedMethod"
      :xPoints="xVector"
      :yPoints="yVector"
    />
</template>

<style scoped></style>
