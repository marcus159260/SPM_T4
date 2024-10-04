<template>
  <DayPilotScheduler :config="config" ref="schedulerRef" />
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, onMounted, watch, defineProps } from 'vue';

const props = defineProps({
  resources: {
    type: Array,
    required: true,
  },
});

const config = reactive({
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
  scale: "CellDuration",
  cellDuration: 720,
  days: DayPilot.Date.today().daysInMonth(),
  startDate: DayPilot.Date.today().firstDayOfMonth(),
  timeRangeSelectedHandling: "Disabled",
  eventClickHandling: "Disabled",
  treeEnabled: true,
  resources: [],
});
const schedulerRef = ref(null);

const loadEvents = () => {
  const events = [
    { id: 1, start: "2024-10-01T00:00:00", end: "2024-10-05T00:00:00", text: "WFH", resource: "R1" },
    { id: 2, start: DayPilot.Date.today(), end: DayPilot.Date.today().addDays(5), text: "WFO", resource: "R2" }
  ];
  config.events = events;
};

watch(
  () => props.resources,
  (newResources) => {
    console.log('Resources updated in hrCalendar.vue:', newResources);
    config.resources = newResources;
  },
  { immediate: true }
);

onMounted(() => {
  loadEvents();
});
</script>
