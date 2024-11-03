<template>
    <CalendarNavigation
    :currentDate="config.startDate"
    :earliestDate="earliestDate"
    :latestDate="latestDate"
    @dateChanged="onDateChanged"
  />
  <DayPilotScheduler :config="config" ref="schedulerRef" />
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, watch, defineProps, defineEmits } from 'vue';
import CalendarNavigation from './CalendarNavigation.vue';

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

const emit = defineEmits(['dateChanged']);

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
  events: [],
  cellWidthSpec: "Auto"
});
const schedulerRef = ref(null);

const today = DayPilot.Date.today();
const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
const daysToMonday = currentDayOfWeek - 1; // Subtract to get back to Monday
const startOfWeek = today.addDays(-daysToMonday);

config.startDate = startOfWeek;

const earliestDate = startOfWeek.addDays(-60); // 60 days back
const latestDate = startOfWeek.addDays(90);    // 90 days forward

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

function onDateChanged(newStartDate) {
  config.startDate = newStartDate;
  emit('dateChanged', newStartDate);
}

</script>
