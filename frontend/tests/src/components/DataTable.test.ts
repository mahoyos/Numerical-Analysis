import { describe, expect, it } from 'vitest';
import { mount } from '@vue/test-utils';

import DataTable from '../../../src/components/DataTable.vue';

describe('DataTable', () => {
  it('paginates rows and moves across pages', async () => {
    const tableData = Array.from({ length: 12 }, (_, index) => ({
      iteration: index + 1,
      value1: index,
      value2: index + 10,
      value3: index / 10,
    }));

    const wrapper = mount(DataTable, {
      props: { tableData },
    });

    expect(wrapper.findAll('tbody tr')).toHaveLength(10);
    expect(wrapper.text()).toContain('Page 1 of 2');

    await wrapper.findAll('button')[1].trigger('click');

    expect(wrapper.findAll('tbody tr')).toHaveLength(2);
    expect(wrapper.text()).toContain('Page 2 of 2');
  });

  it('does not go below first page or beyond last page', async () => {
    const tableData = Array.from({ length: 11 }, (_, index) => ({
      iteration: index + 1,
      value1: index,
      value2: index + 10,
      value3: index / 10,
    }));

    const wrapper = mount(DataTable, {
      props: { tableData },
    });

    const [previousButton, nextButton] = wrapper.findAll('button');

    await previousButton.trigger('click');
    expect(wrapper.text()).toContain('Page 1 of 2');

    await nextButton.trigger('click');
    await nextButton.trigger('click');
    expect(wrapper.text()).toContain('Page 2 of 2');
  });
});