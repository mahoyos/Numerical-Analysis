import { createRouter, createWebHistory } from 'vue-router';

import NonLinearEquationsView from '../views/NonLinearEquationsView.vue';
import HomeView from '../views/HomeView.vue';
import EquationsSystemsView from '../views/EquationsSystemsView.vue';
import FixedPointView from '../views/NonLinearEquations/FixedPoint.vue';
import NewtonRaphsonView from '../views/NonLinearEquations/NewtonRaphson.vue';
import MultipleRootsView from '../views/NonLinearEquations/MultipleRoots.vue';
import FalsePositionView from '../views/NonLinearEquations/FalsePosition.vue';
import BisectionView from '../views/NonLinearEquations/Bisection.vue';
import SecantView from '../views/NonLinearEquations/Secant.vue';
import InterpolationsView from '../views/InterpolationsView.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/non-linear-equations',
      name: 'non-linear-equations',
      component: NonLinearEquationsView
    },
    {
      path: '/equations-systems',
      name: 'equations-systems',
      component: EquationsSystemsView
    },
    {
      path: '/fixed-point',
      name: 'fixed-point',
      component: FixedPointView
    },
    {
      path: '/newton-raphson',
      name: 'newton-raphson',
      component: NewtonRaphsonView
    },
    {
      path: '/multiple-roots',
      name: 'multiple-roots',
      component: MultipleRootsView
    },
    {
      path: '/false-position',
      name: 'false-position',
      component: FalsePositionView
    },
    {
      path: '/bisection',
      name: 'bisection',
      component: BisectionView
    },
    {
      path: '/secant',
      name: 'secant',
      component: SecantView
    },
    {
      path: '/interpolations',
      name: 'interpolations',
      component: InterpolationsView
    }
  ]
});

export default router;
