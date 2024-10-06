<script setup lang="ts">
import { ref } from 'vue';

defineProps<{
  title: string
}>();

const launchButton = ref<HTMLButtonElement | null>(null);
const closeButton = ref<HTMLButtonElement | null>(null);
let message = ref('');
let modalFooter = ref(false);
let status = ref('success');

const launch = () => {
  if (launchButton.value) {
    launchButton.value.click();
  }
};

const close = async () => {
  setTimeout(function () {
    if (closeButton.value) {
      closeButton.value.click();
    }
  }, 1000);
};

const modifyMessage = (newMessage: string, newStatus: string) => {
  message.value = newMessage;
  status.value = newStatus;
  modalFooter.value = true;
};

const clear = () => {
  modalFooter.value = false;
  message.value = '';
};

defineExpose({
  launch,
  close,
  modifyMessage
});
</script>

<template>
  <button ref="launchButton" type="button" class="d-none" data-bs-toggle="modal" data-bs-target="#staticBackdrop">
    Hidden button
  </button>

  <!-- Modal -->
  <div class="modal fade" id="staticBackdrop" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
    aria-labelledby="staticBackdropLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">{{ title }}</h5>
          <button ref="closeButton" type="button" class="btn-close" data-bs-dismiss="modal" @click="clear" aria-label="Close"></button>
        </div>
        <div class="modal-body text-center">
          <div v-if="message" :class="{ 'text-success': status === 'success', 'text-danger': status === 'error' }">
            <b>{{ message }}</b>
          </div>
          <div v-else id="modal-spinner" class="justify-content-center v-display mbottom20">
            <div class="spinner-border text-primary" role="status">
              <span class="sr-only">Loading...</span>
            </div>
          </div>
        </div>
        <div class="modal-footer" v-if="modalFooter">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="clear">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
</template>