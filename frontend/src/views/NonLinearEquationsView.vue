<script setup lang='ts'>
import BreadCrumb from '../components/BreadCrumb.vue';

const breadCrumbList = [
  {
    title: 'Home', route: '/',
  },
  {
    title: 'Non-Linear Equations', route: 'non-linear-equations' 
  },
];

const methods = [
  {
    name: 'Bisection',
    route: '/bisection',
    description: 'A root-finding method that repeatedly bisects an interval and selects a subinterval where a root exists.'
  },
  {
    name: 'Fixed Point',
    route: '/fixed-point',
    description: 'Finds a solution by iteratively calculating a function value until it converges to a fixed point.'
  },
  {
    name: 'False Position',
    route: '/false-position',
    description: 'Also known as regula falsi, uses linear interpolation to find better approximations of roots.'
  },
  {
    name: 'Newton-Raphson',
    route: '/newton-raphson',
    description: 'Uses function derivatives to find successively better approximations of roots.'
  },
  {
    name: 'Multiple Roots',
    route: '/multiple-roots',
    description: 'Modified Newton method for finding roots with multiplicity greater than one.'
  },
  {
    name: 'Secant',
    route: '/secant',
    description: 'Similar to Newton method but uses finite difference instead of derivatives.'
  }
];

const functionExamples = [
  {
    title: 'Basic Operations',
    examples: [
      { operation: 'Addition/Subtraction', syntax: 'x + 2, x - 1' },
      { operation: 'Multiplication', syntax: '2*x, -3*x' },
      { operation: 'Division', syntax: '2/x, 1/(x+1)' },
    ]
  },
  {
    title: 'Powers and Roots',
    examples: [
      { operation: 'Powers', syntax: 'x**2, (x+1)**3' },
      { operation: 'Square root', syntax: 'x**(1/2)' },
      { operation: 'Cube root', syntax: 'x**(1/3)' },
    ]
  },
  {
    title: 'Trigonometric Functions',
    examples: [
      { operation: 'Basic', syntax: 'sin(x), cos(x), tan(x)' },
      { operation: 'Inverse', syntax: 'asin(x), acos(x), atan(x)' },
    ]
  },
  {
    title: 'Exponential and Logarithms',
    examples: [
      { operation: 'Exponential', syntax: 'exp(x)' },
      { operation: 'Natural logarithm', syntax: 'log(x)' },
      { operation: 'Custom base logarithm', syntax: 'log(x, base)' },
    ]
  }
];
</script>

<template>
  <BreadCrumb :breadCrumbList="breadCrumbList" />

  <div class="card shadow mb-4">
    <div class="card-header py-3">
      <h4 class="m-0 font-weight-bold text-primary">Non-Linear Equations</h4>
    </div>
    <div class="card-body">
      <p class="lead mb-4">
        This section provides various numerical methods for finding roots of non-linear equations.
        Each method has its own characteristics and is suitable for different types of problems.
      </p>

      <!-- Function Input Format Section -->
      <div class="card mb-4">
        <div class="card-header py-3">
          <h5 class="m-0 font-weight-bold text-primary">Function Input Format</h5>
        </div>
        <div class="card-body">
          <p class="mb-4">
            When entering functions, please use the following format and available operations:
          </p>
          
          <div class="row row-cols-1 row-cols-md-2">
            <!-- Basic Operations -->
            <div class="col mb-4">
              <h6 class="font-weight-bold">Basic Operations</h6>
              <div class="table-responsive">
                <table class="table table-bordered h-100">
                  <thead>
                    <tr>
                      <th width="50%">Operation</th>
                      <th width="50%">Syntax</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Addition/Subtraction</td>
                      <td><code>x + 2, x - 1</code></td>
                    </tr>
                    <tr>
                      <td>Multiplication</td>
                      <td><code>2*x, -3*x</code></td>
                    </tr>
                    <tr>
                      <td>Division</td>
                      <td><code>2/x, 1/(x+1)</code></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Powers and Roots -->
            <div class="col mb-4">
              <h6 class="font-weight-bold">Powers and Roots</h6>
              <div class="table-responsive">
                <table class="table table-bordered h-100">
                  <thead>
                    <tr>
                      <th width="50%">Operation</th>
                      <th width="50%">Syntax</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Powers</td>
                      <td><code>x**2, (x+1)**3</code></td>
                    </tr>
                    <tr>
                      <td>Square root</td>
                      <td><code>x**(1/2)</code></td>
                    </tr>
                    <tr>
                      <td>Cube root</td>
                      <td><code>x**(1/3)</code></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Trigonometric Functions -->
            <div class="col mb-4">
              <h6 class="font-weight-bold">Trigonometric Functions</h6>
              <div class="table-responsive">
                <table class="table table-bordered h-100">
                  <thead>
                    <tr>
                      <th width="50%">Operation</th>
                      <th width="50%">Syntax</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Basic</td>
                      <td><code>sin(x), cos(x), tan(x)</code></td>
                    </tr>
                    <tr>
                      <td>Inverse</td>
                      <td><code>asin(x), acos(x), atan(x)</code></td>
                    </tr>
                    <tr>
                      <td>&nbsp;</td>
                      <td>&nbsp;</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>

            <!-- Exponential and Logarithms -->
            <div class="col mb-4">
              <h6 class="font-weight-bold">Exponential and Logarithms</h6>
              <div class="table-responsive">
                <table class="table table-bordered h-100">
                  <thead>
                    <tr>
                      <th width="50%">Operation</th>
                      <th width="50%">Syntax</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr>
                      <td>Exponential</td>
                      <td><code>exp(x)</code></td>
                    </tr>
                    <tr>
                      <td>Natural logarithm</td>
                      <td><code>log(x)</code></td>
                    </tr>
                    <tr>
                      <td>Custom base logarithm</td>
                      <td><code>log(x, base)</code></td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <div class="alert alert-info">
            <i class="fas fa-info-circle me-2"></i>
            Remember to use parentheses to group operations when needed. For example: <code>(x+1)/(x-2)</code>
          </div>
        </div>
      </div>
      <div class="card-header py-3">
        <h5 class="m-0 font-weight-bold text-primary">Available Methods</h5>
      </div>
      <!-- Methods Section -->
      <div class="methods-grid">
        <div v-for="method in methods" :key="method.name" class="method-card">
          <div class="card h-100">
            <div class="card-body">
              <h5 class="card-title">{{ method.name }}</h5>
              <p class="card-text">{{ method.description }}</p>
              <router-link 
                :to="method.route" 
                class="btn btn-outline-primary"
              >
                Try {{ method.name }}
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.card-text {
  margin-bottom: 1rem;
}

.g-4 {
  gap: 1.5rem;
}

code {
  background-color: #f8f9fa;
  padding: 0.2rem 0.4rem;
  border-radius: 0.2rem;
}

.table {
  margin-bottom: 0;
}

.table td, .table th {
  padding: 0.5rem;
}

.me-2 {
  margin-right: 0.5rem;
}

.row {
  margin-right: 0;
  margin-left: 0;
}

.col {
  padding: 0.75rem;
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

/* Para pantallas pequeñas */
@media (max-width: 768px) {
  .methods-grid {
    grid-template-columns: 1fr;
  }
}
</style>
