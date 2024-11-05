<template>
  <div width=100% ref="customDiv">
    <div v-if="showPopup" @click.stop class="popup-container">
      <div class="popup-content">
        <slot name="content"/>
        <div class="d-flex justify-content-end my-4">
          <button type="button" class="btn btn-light border border-secondary" @click="closePopup">Close</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, defineProps, defineEmits, watch } from 'vue'

const props = defineProps({
  visible: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:visible'])
const showPopup = ref(props.visible)

const closePopup = () => {
  emit('update:visible', false)
}

onMounted(() => {
  showPopup.value = props.visible
})

watch(() => props.visible, (newValue) => {
  showPopup.value = newValue
})
</script>

<style scoped>
.popup-container {
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent overlay */
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background-color: white; /* White background for the popup content */
  padding: 20px;
  border-radius: 8px;
  border: 2px solid #ccc; /* Add a border */
  width: 440px; /* Adjust width as needed */
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2); /* Optional shadow for depth */
}
</style>
