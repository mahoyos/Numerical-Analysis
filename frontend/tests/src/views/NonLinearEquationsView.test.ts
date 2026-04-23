import { describe, expect, it } from 'vitest';
import { mount } from '@vue/test-utils';

import NonLinearEquationsView from '../../../src/views/NonLinearEquationsView.vue';

describe('NonLinearEquationsView', () => {
  it('renders the methods overview and action links', () => {
    const wrapper = mount(NonLinearEquationsView, {
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

    expect(wrapper.text()).toContain('Non-Linear Equations');
    expect(wrapper.text()).toContain('Available Methods');
    expect(wrapper.findAll('a')).toHaveLength(6);
  });
});