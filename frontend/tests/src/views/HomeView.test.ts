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

    expect(wrapper.text()).toContain('Welcome to Numerical Methods Calculator');
    expect(wrapper.text()).toContain('Non-Linear Equations');
    expect(wrapper.text()).toContain('Systems of Equations');
    expect(wrapper.text()).toContain('Interpolation');
    expect(wrapper.findAll('a')).toHaveLength(8);
  });
});