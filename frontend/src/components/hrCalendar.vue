<template>
  <DayPilotScheduler :config="config" ref="schedulerRef" />
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, watch, defineProps } from 'vue';

const props = defineProps({
  resources: {
    type: Array,
    required: true,
  },
  events: {
    type: Array,
    required: true,
  },
});

const config = reactive({
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
  scale: "CellDuration",
  cellDuration: 720,
  // days: DayPilot.Date.today().daysInMonth(),
  days: 7,
  startDate: DayPilot.Date.today().firstDayOfMonth(),
  timeRangeSelectedHandling: "Disabled",
  eventClickHandling: "Disabled",
  treeEnabled: true,
  resources: [],
  events: []
});
const schedulerRef = ref(null);

// Watch for changes in resources prop
watch(
  () => props.resources,
  (newResources) => {
    // console.log('Resources updated in hrCalendar.vue:', newResources);
    config.resources = newResources;
  },
  { immediate: true }
);

// Watch for changes in events prop
watch(
  () => props.events,
  (newEvents) => {
    // console.log('Events updated in hrCalendar.vue:', newEvents);
    config.events = newEvents;
  },
  { immediate: true }
);

</script>
