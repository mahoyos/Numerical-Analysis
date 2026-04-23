import { beforeEach, describe, expect, it, vi } from 'vitest';
import { flushPromises, mount } from '@vue/test-utils';

import InterpolationsService from '../../../src/services/InterpolationsService';
import InterpolationsView from '../../../src/views/InterpolationsView.vue';

vi.mock('../../../src/services/InterpolationsService', () => ({
  default: {
    postInterpolationsData: vi.fn(),
  },
}));

describe('InterpolationsView', () => {
  beforeEach(() => {
    vi.mocked(InterpolationsService.postInterpolationsData).mockReset();
  });

  it('renders the interpolation page', () => {
    const wrapper = mount(InterpolationsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          InterpolationGraph: {
            template: '<div />',
          },
        },
      },
    });

    expect(wrapper.text()).toContain('Interpolation Methods');
    expect(wrapper.text()).toContain('Interpolation Calculator');
  });

  it('rejects repeated x values before calling the API', async () => {
    const wrapper = mount(InterpolationsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          InterpolationGraph: {
            template: '<div />',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[1].setValue(1);
    await inputs[2].setValue(1);
    await inputs[3].setValue(3);
    await inputs[4].setValue(4);

    await wrapper.find('form').trigger('submit');

    expect(wrapper.text()).toContain('X values must be unique');
    expect(InterpolationsService.postInterpolationsData).not.toHaveBeenCalled();
  });

  it('submits valid data and renders the result polynomial', async () => {
    vi.mocked(InterpolationsService.postInterpolationsData).mockResolvedValue({
      polynom: 'x**2 + 1',
    });

    const wrapper = mount(InterpolationsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          InterpolationGraph: {
            template: '<div />',
          },
        },
      },
    });

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[1].setValue(1);
    await inputs[2].setValue(2);
    await inputs[3].setValue(3);
    await inputs[4].setValue(4);

    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(InterpolationsService.postInterpolationsData).toHaveBeenCalledTimes(1);
    expect(wrapper.text()).toContain('Interpolation Result');
    expect(wrapper.text()).toContain('f(x) = x**2 + 1');
  });

  it('validates spline degree before calling the API', async () => {
    const wrapper = mount(InterpolationsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          InterpolationGraph: {
            template: '<div />',
          },
        },
      },
    });

    const methodSelect = wrapper.get('#methodSelect');
    await methodSelect.setValue('spline');

    const degreeInput = wrapper.get('#degree');
    await degreeInput.setValue(3);

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[2].setValue(1);
    await inputs[3].setValue(2);
    await inputs[4].setValue(3);
    await inputs[5].setValue(4);

    await wrapper.find('form').trigger('submit');

    expect(wrapper.text()).toContain('degree must be either 1 or 2');
    expect(InterpolationsService.postInterpolationsData).not.toHaveBeenCalled();
  });

  it('renders spline segments when API returns piecewise polynomial', async () => {
    vi.mocked(InterpolationsService.postInterpolationsData).mockResolvedValue({
      polynom: "['x + 1', '2*x + 3']",
    });

    const wrapper = mount(InterpolationsView, {
      global: {
        stubs: {
          BreadCrumb: {
            template: '<div />',
          },
          InterpolationGraph: {
            template: '<div />',
          },
        },
      },
    });

    await wrapper.get('#methodSelect').setValue('spline');
    await wrapper.get('#degree').setValue(1);

    const inputs = wrapper.findAll('input[type="number"]');
    await inputs[2].setValue(1);
    await inputs[3].setValue(2);
    await inputs[4].setValue(3);
    await inputs[5].setValue(4);

    await wrapper.find('form').trigger('submit');
    await flushPromises();

    expect(wrapper.text()).toContain('Piecewise Polynomials:');
    expect(wrapper.text()).toContain('Segment 1:');
    expect(wrapper.text()).toContain('f(x) = x + 1');
  });
});