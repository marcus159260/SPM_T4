<template>
    <div class="scheduler-container">
      <button @click="goPreviousWeek" :disabled="isPreviousDisabled">Previous Week</button>
      <button @click="goNextWeek" :disabled="isNextDisabled">Next Week</button>
    </div>
  </template>
<script setup>
import { computed, defineProps, defineEmits } from 'vue';
import { DayPilot } from 'daypilot-pro-vue';
const props = defineProps({
  currentDate: {
    type: DayPilot.Date,
    required: true,
  },
  earliestDate: {
    type: DayPilot.Date, 
    required: true,
  },
  latestDate: {
    type: DayPilot.Date, 
    required: true,
  },
});
const emit = defineEmits(['dateChanged']);
function goPreviousWeek() {
  const newStartDate = props.currentDate.addDays(-7);
  if (newStartDate.getTime() >= props.earliestDate.getTime()) {
    emit('dateChanged', newStartDate);
  }
}
function goNextWeek() {
  const newStartDate = props.currentDate.addDays(7);
  if (newStartDate.getTime() <= props.latestDate.getTime()) {
    emit('dateChanged', newStartDate);
  }
}
const isPreviousDisabled = computed(() => {
  return props.currentDate.getTime() <= props.earliestDate.getTime();
});
const isNextDisabled = computed(() => {
  return props.currentDate.getTime() >= props.latestDate.getTime();
});
</script>
<style scoped>
.scheduler-container {
  display: flex;
  justify-content: center;
  margin-bottom: 10px;
}
button {
  margin: 0 5px;
}
</style>