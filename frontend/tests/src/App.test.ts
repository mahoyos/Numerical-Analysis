import { describe, expect, it } from 'vitest';
import { mount } from '@vue/test-utils';

import App from '../../src/App.vue';

describe('App', () => {
  it('toggles sidebar classes when the sidebar button is clicked', async () => {
    const wrapper = mount(App, {
      attachTo: document.body,
      global: {
        stubs: {
          RouterLink: {
            template: '<a><slot /></a>',
          },
          RouterView: {
            template: '<div />',
          },
        },
      },
    });

    expect(document.body.classList.contains('sidebar-toggled')).toBe(false);

    await wrapper.get('#sidebarToggle').trigger('click');

    expect(document.body.classList.contains('sidebar-toggled')).toBe(true);
    expect(wrapper.find('.sidebar').classes()).toContain('toggled');
    expect(wrapper.find('#main-icon').classes()).toContain('display-icon-yes');
    expect(wrapper.find('#main-text').classes()).toContain('d-none');

    wrapper.unmount();
    document.body.classList.remove('sidebar-toggled');
  });
});