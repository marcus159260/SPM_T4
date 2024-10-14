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
  startDate: DayPilot.Date.today(),
  timeRangeSelectedHandling: "Disabled",
  eventClickHandling: "Disabled",
  treeEnabled: true,
  resources: [],
  events: []
});
const schedulerRef = ref(null);

watch(
  () => props.resources,
  (newResources) => {
    config.resources = newResources;
  },
  { immediate: true }
);

watch(
  () => props.events,
  (newEvents) => {
    config.events = newEvents;
  },
  { immediate: true }
);

</script>
