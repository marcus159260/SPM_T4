<template>
    <div width=100% ref="customDiv">
      <div v-if="showPopup" @click.stop>
        <slot name="content"/>
        <div class="d-flex justify-content-end my-4">
            <button type="button" class="btn btn-light border border-secondary" @click="closePopup">Close</button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { onMounted, onUnmounted, ref, defineProps, defineEmits, watch } from 'vue'
  
  const props = defineProps({
    visible: {
      type: Boolean,
      default: false
    }
  })
  
  const emit = defineEmits(['update:visible'])
  
  const customDiv = ref(null)
  const showPopup = ref(props.visible)
  
  const closePopup = () => {
    emit('update:visible', false)
    document.getElementById('popup').style.display = 'none';
  }
  
  onMounted(() => {
    showPopup.value = props.visible
  })
  
  onUnmounted(() => {})
  
  // Watch for changes in the visible prop
  watch(() => props.visible, (newValue) => {
    showPopup.value = newValue
  })
  </script>
  