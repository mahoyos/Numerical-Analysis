import { describe, expect, it } from 'vitest';
import { mount } from '@vue/test-utils';

import SystemsEquationsDataTable from '../../../src/components/SystemsEquationsDataTable.vue';

describe('SystemsEquationsDataTable', () => {
  it('renders first page with 5 rows by default', () => {
    const tableData = Array.from({ length: 12 }, (_, i) => ({
      iteration: i + 1,
      values: [i, i + 1],
      error: i / 10,
    }));

    const wrapper = mount(SystemsEquationsDataTable, {
      props: { tableData },
    });

    const rows = wrapper.findAll('tbody > tr');
    expect(rows.length).toBe(5);
    expect(wrapper.text()).toContain('Page 1 of 3');
  });

  it('navigates to next page', async () => {
    const tableData = Array.from({ length: 12 }, (_, i) => ({
      iteration: i + 1,
      values: [i, i + 1],
      error: i / 10,
    }));

    const wrapper = mount(SystemsEquationsDataTable, {
      props: { tableData },
    });

    const buttons = wrapper.findAll('button');
    await buttons[1].trigger('click');

    expect(wrapper.text()).toContain('Page 2 of 3');
  });
});
