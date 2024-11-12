<script setup lang='ts'>
import BreadCrumb from '../components/BreadCrumb.vue';

const breadCrumbList = [
  {
    title: 'Home', 
    route: '/',
  }
];

const sections = [
  {
    title: 'Non-Linear Equations',
    description: 'Collection of methods for finding roots of non-linear equations',
    methods: [
      { name: 'Fixed Point', route: '/fixed-point' },
      { name: 'Newton-Raphson', route: '/newton-raphson' },
      { name: 'Multiple Roots', route: '/multiple-roots' },
      { name: 'False Position', route: '/false-position' },
      { name: 'Bisection', route: '/bisection' },
      { name: 'Secant', route: '/secant' }
    ]
  },
  {
    title: 'Systems of Equations',
    description: 'Methods for solving systems of linear and non-linear equations. Includes Jacobi Method, Gauss-Seidel Method, and SOR (Successive Over-Relaxation)',
    methods: [
      { name: 'Equations Systems', route: '/equations-systems' }
    ]
  },
  {
    title: 'Interpolation',
    description: 'Techniques for constructing new data points within a discrete set of known points. Includes Newton Interpolation, Linear Spline, Quadratic Spline, Vandermonde, and Lagrange methods',
    methods: [
      { name: 'Interpolations', route: '/interpolations' }
    ]
  }
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <!-- Welcome Section -->
  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h4 class="m-0 font-weight-bold text-primary">Welcome to Numerical Methods Calculator</h4>
    </div>
    <div class="card-body">
      <p class="lead">
        This application provides a comprehensive suite of numerical methods for solving various mathematical problems.
        Choose from our collection of implemented methods below to get started.
      </p>
    </div>
  </div>

  <!-- Methods Sections -->
  <div v-for="section in sections" :key="section.title" class="card shadow mb-4">
    <div class="card-header py-3">
      <h5 class="m-0 font-weight-bold text-primary">{{ section.title }}</h5>
    </div>
    <div class="card-body">
      <p class="mb-3">{{ section.description }}</p>
      <div class="d-flex flex-wrap gap-2">
        <router-link 
          v-for="method in section.methods" 
          :key="method.name"
          :to="method.route" 
          class="btn btn-outline-primary"
        >
          {{ method.name }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<style scoped>
.gap-2 {
  gap: 0.5rem;
}
</style>
