import { describe, expect, it } from 'vitest';
import { mount } from '@vue/test-utils';

import HomeView from '../../../src/views/HomeView.vue';

describe('HomeView', () => {
  it('renders the main landing sections', () => {
    const wrapper = mount(HomeView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          RouterLink: {
            template: '<a><slot /></a>',
          },
        },
      },
    });

    expect(wrapper.text()).toContain('Welcome to Numerical Methods Calculators');
    expect(wrapper.text()).toContain(
      'This application provides a comprehensive suite of numerical methods for solving various mathematical problems.'
    );
    expect(wrapper.text()).toContain('Non-Linear Equations');
    expect(wrapper.text()).toContain('Collection of methods for finding roots of non-linear equation');
    expect(wrapper.text()).toContain('Fixed Point');
    expect(wrapper.text()).toContain('Newton-Raphson');
    expect(wrapper.text()).toContain('Multiple Roots');
    expect(wrapper.text()).toContain('False Position');
    expect(wrapper.text()).toContain('Bisection');
    expect(wrapper.text()).toContain('Secant');
    expect(wrapper.text()).toContain('Systems of Equations');
    expect(wrapper.text()).toContain(
      'Methods for solving systems of linear and non-linear equation. Includes Jacobi Method, Gauss-Seidel Method, and SOR (Successive Over-Relaxation)'
    );
    expect(wrapper.text()).toContain('Equations Systems');
    expect(wrapper.text()).toContain('Interpolation');
    expect(wrapper.text()).toContain(
      'Techniques for constructing new data points within a discrete set of known points. Includes Newton Interpolation, Linear Spline, Quadratic Spline, Vandermonde, and Lagrange methods'
    );
    expect(wrapper.text()).toContain('Interpolations');
    expect(wrapper.findAll('a')).toHaveLength(8);
  });
});
