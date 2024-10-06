import { createRouter, createWebHistory } from 'vue-router';

import NonLinearEquationsView from '../views/NonLinearEquationsView.vue';
import HomeView from '../views/HomeView.vue';
import EquationsSystemsView from '../views/EquationsSystemsView.vue';
import FixedPointView from '../views/NonLinearEquations/FixedPoint.vue';
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
  ]
});

export default router;
