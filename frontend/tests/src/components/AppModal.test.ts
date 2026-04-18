import { describe, expect, it, vi } from 'vitest';
import { mount } from '@vue/test-utils';

import AppModal from '../../../src/components/AppModal.vue';

describe('AppModal', () => {
  it('updates exposed message and status', async () => {
    const wrapper = mount(AppModal, { props: { title: 'My Modal' } });

    (wrapper.vm as any).modifyMessage('Saved', 'success');
    await wrapper.vm.$nextTick();

    expect(wrapper.text()).toContain('Saved');
  });

  it('launch triggers hidden button click', () => {
    const wrapper = mount(AppModal, { props: { title: 'My Modal' } });
    const hiddenButton = wrapper.find('button.d-none');
    const clickSpy = vi.spyOn(hiddenButton.element as HTMLButtonElement, 'click');

    (wrapper.vm as any).launch();

    expect(clickSpy).toHaveBeenCalledTimes(1);
  });

  it('close triggers delayed click on close button', async () => {
    vi.useFakeTimers();
    const wrapper = mount(AppModal, { props: { title: 'My Modal' } });
    const closeButton = wrapper.find('button.btn-close');
    const clickSpy = vi.spyOn(closeButton.element as HTMLButtonElement, 'click');

    await (wrapper.vm as any).close();
    vi.advanceTimersByTime(1000);

    expect(clickSpy).toHaveBeenCalledTimes(1);
    vi.useRealTimers();
  });
});
