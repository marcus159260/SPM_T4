<template>
    <br>
    <div class="scheduler-container">
      <button class="btn-outline-dark btn" @click="goPreviousWeek" :disabled="isPreviousDisabled">Previous Week</button>
      <button class="btn-outline-dark btn" @click="goNextWeek" :disabled="isNextDisabled">Next Week</button>
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
    emit('dateChanged', newStartDate.firstDayOfWeek().addDays(1));
  }
}

function goNextWeek() {
  const newStartDate = props.currentDate.addDays(7);
  if (newStartDate.getTime() <= props.latestDate.getTime()) {
    emit('dateChanged', newStartDate.firstDayOfWeek().addDays(1));
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

