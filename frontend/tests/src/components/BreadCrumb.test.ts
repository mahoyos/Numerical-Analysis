import { describe, expect, it } from 'vitest';
import { createMemoryHistory, createRouter } from 'vue-router';
import { mount } from '@vue/test-utils';

import BreadCrumb from '../../../src/components/BreadCrumb.vue';

const router = createRouter({
  history: createMemoryHistory(),
  routes: [
    { path: '/', component: { template: '<div>home</div>' } },
    { path: '/non-linear-equations', component: { template: '<div>nle</div>' } },
  ],
});

describe('BreadCrumb', () => {
  it('renders link and text items', async () => {
    const wrapper = mount(BreadCrumb, {
      props: {
        breadCrumbList: [
          { title: 'Home', route: '/' },
          { title: 'Current', route: '' },
        ],
      },
      global: {
        plugins: [router],
      },
    });

    await router.isReady();

    expect(wrapper.text()).toContain('Home');
    expect(wrapper.text()).toContain('Current');
    expect(wrapper.findAll('a').length).toBe(1);
  });
});
