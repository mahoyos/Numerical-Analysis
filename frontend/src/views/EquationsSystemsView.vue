<script setup lang='ts'>
import BreadCrumb from '../components/BreadCrumb.vue';

let breadCrumbList = [
  {
    title: 'Home', route: '/',
  },
  {
    title: 'Equations Systems', route: 'equations-systems' 
  },
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Equations Systems</h6>
    </div>
    <div class="card-body">
      <button type="button" class="btn btn-outline-primary">Bisection</button>
      <button type="button" class="btn btn-outline-primary">Fixed Point</button>
      <button type="button" class="btn btn-outline-primary">False Position</button>
      <button type="button" class="btn btn-outline-primary">Newton-Raphson</button>
      <button type="button" class="btn btn-outline-primary">Multiple Roots</button>
    </div>
  </div>
</template>

<style scoped></style>
