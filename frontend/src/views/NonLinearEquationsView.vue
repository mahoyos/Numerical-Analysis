<script setup lang='ts'>
import BreadCrumb from '../components/BreadCrumb.vue';

let breadCrumbList = [
  {
    title: 'Home', route: '/',
  },
  {
    title: 'Non-Linear Equations', route: 'non-linear-equations' 
  },
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Non-Linear Equations</h6>
    </div>
    <div class="card-body">
      <router-link to="/bisection" class="btn btn-outline-primary">Bisection</router-link>
      <router-link to="/fixed-point" class="btn btn-outline-primary">Fixed Point</router-link>
      <router-link to="/false-position" class="btn btn-outline-primary">False Position</router-link>
      <router-link to="/newton-raphson" class="btn btn-outline-primary">Newton-Raphson</router-link>
      <router-link to="/multiple-roots" class="btn btn-outline-primary">Multiple Roots</router-link>
      <router-link to="/secant" class="btn btn-outline-primary">Secant</router-link>
    </div>
  </div>
</template>

<style scoped></style>
