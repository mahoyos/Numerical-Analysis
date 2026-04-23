import { beforeEach, describe, expect, it, vi } from 'vitest';
import { flushPromises, mount } from '@vue/test-utils';

import SystemsEquationsService from '../../../src/services/SystemsEquationsService';
import EquationsSystemsView from '../../../src/views/EquationsSystemsView.vue';

vi.mock('../../../src/services/SystemsEquationsService', () => ({
  default: {
    postSystemsEquationsData: vi.fn(),
  },
}));

describe('EquationsSystemsView', () => {
  beforeEach(() => {
    vi.mocked(SystemsEquationsService.postSystemsEquationsData).mockReset();
  });

  it('renders the system solver page', () => {
    const wrapper = mount(EquationsSystemsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          LineGraph: {
            template: '<div />',
          },
        },
      },
    });

    expect(wrapper.text()).toContain('Systems of Linear Equations');
    expect(wrapper.text()).toContain('System Solver Calculator');
    expect(wrapper.text()).toContain('Methods Comparison');
  });

  it('submits the form and renders the solution summary', async () => {
    vi.mocked(SystemsEquationsService.postSystemsEquationsData).mockResolvedValue({
      status: 'success',
      iterations: [[1, [1.1, 2.2], 0.05]],
      root: [1.1, 2.2],
      spectral_radius: 0.4,
    });

    const wrapper = mount(EquationsSystemsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          LineGraph: {
            template: '<div />',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[0].setValue(15);
    await inputs[1].setValue(0.001);
    await inputs[2].setValue(2);
    await inputs[3].setValue(4);
    await inputs[4].setValue(1);
    await inputs[5].setValue(2);
    await inputs[6].setValue(3);
    await inputs[7].setValue(5);
    await inputs[8].setValue(6);
    await inputs[9].setValue(0);
    await inputs[10].setValue(0);

    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(SystemsEquationsService.postSystemsEquationsData).toHaveBeenCalledTimes(1);
    expect(wrapper.text()).toContain('Final Solution:');
    expect(wrapper.text()).toContain('x1 = 1.100000');
    expect(wrapper.text()).toContain('ρ = 0.400000');
  });

  it('shows convergence guidance when backend returns convergence error', async () => {
    vi.mocked(SystemsEquationsService.postSystemsEquationsData).mockResolvedValue({
      status: 'error',
      error: {
        code: 'CONVERGENCE_ERROR',
        message: 'did not converge',
      },
    });

    const wrapper = mount(EquationsSystemsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          LineGraph: {
            template: '<div />',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[0].setValue(20);
    await inputs[1].setValue(0.001);
    await inputs[2].setValue(2);

    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(wrapper.text()).toContain('failed to converge');
    expect(wrapper.text()).toContain('Jacobi method requires');
  });

  it('shows unknown error message when request throws', async () => {
    vi.mocked(SystemsEquationsService.postSystemsEquationsData).mockRejectedValue(new Error('network'));

    const wrapper = mount(EquationsSystemsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          LineGraph: {
            template: '<div />',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[0].setValue(20);
    await inputs[1].setValue(0.001);
    await inputs[2].setValue(2);

    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(wrapper.text()).toContain('UNKNOWN_ERROR');
  });
});