<script setup lang="ts">
import { ref, watch } from 'vue';
import BreadCrumb from '../components/BreadCrumb.vue';

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

// Inicialización de matrixValues para el tamaño inicial
matrixValues.value = Array.from({ length: matrixSize.value }, () => Array(matrixSize.value).fill(0));

// Observador para actualizar matrixValues cuando cambia el tamaño
watch(matrixSize, (newSize) => {
  matrixValues.value = Array.from({ length: Number(newSize) }, () => Array(Number(newSize)).fill(0));
});

</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Equations Systems</h6>
    </div>
    <form class="p-4">
      <div class="form-group">
        <label for="methodSelect">Choose a method:</label>
        <select id="methodSelect" v-model="selectedMethod" class="form-control">
          <option value="jacobi">Jacobi</option>
          <option value="gauss-seidel">Gauss-Seidel</option>
          <option value="sor">SOR</option>
        </select>
      </div>
      
      <!-- Input para tamaño de la matriz -->
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

      <!-- Inputs para los valores de la matriz -->
      <div v-if="matrixSize" class="mt-3">
        <label>Matriz {{ matrixSize }}x{{ matrixSize }}</label>
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
      
      <button type="submit" class="btn btn-primary mt-3">Submit</button>
    </form>
  </div>
</template>

<style scoped></style>
