<script setup lang='ts'>
import BreadCrumb from '../components/BreadCrumb.vue';

let breadCrumbList = [
  {
    title: 'Home', route: '/',
  }
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h6 class="m-0 font-weight-bold text-primary">Non-Linear Equations</h6>
    </div>
    <div class="card-body">
      <button type="button" class="btn btn-outline-primary">Primary</button>
      <button type="button" class="btn btn-outline-secondary">Secondary</button>
      <button type="button" class="btn btn-outline-success">Success</button>
      <button type="button" class="btn btn-outline-danger">Danger</button>
      <button type="button" class="btn btn-outline-warning">Warning</button>
    </div>
  </div>
</template>

<style scoped></style>
