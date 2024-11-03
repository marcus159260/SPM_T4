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
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},
  // {"groupBy":"Cell","format":"tt"}
  { groupBy: "Cell", format: "tt" },
],
  scale: "Manual",
  cellDuration: 720,
  days: 7,
  timeRangeSelectedHandling: "Disabled",
  eventClickHandling: "Disabled",
  treeEnabled: true,
  resources: [],
  events: [],
  cellWidthSpec: "Auto",
});

const schedulerRef = ref(null);

const today = DayPilot.Date.today();
const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
const daysToMonday = currentDayOfWeek - 1; // Subtract to get back to Monday
const startOfWeek = today.addDays(-daysToMonday);

config.startDate = startOfWeek;

const earliestDate = startOfWeek.addDays(-60); // 60 days back
const latestDate = startOfWeek.addDays(90);    // 90 days forward

function onDateChanged(newStartDate) {
  config.startDate = newStartDate;
  emit('dateChanged', newStartDate);
}

function generateTimeline(startDate, days) {
  const timeline = [];
  for (let i = 0; i < days; i++) {
    const day = startDate.addDays(i);
    const date = day.toString("yyyy-MM-dd");
    timeline.push({
      start: date + "T09:00:00",
      end: date + "T13:00:00",
      label: "AM",
    });
    timeline.push({
      start: date + "T13:00:00",
      end: date + "T18:00:00",
      label: "PM",
    });
  }
  return timeline;
}

config.timeline = generateTimeline(config.startDate, config.days);

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

watch(
  () => config.startDate,
  (newStartDate) => {
    config.timeline = generateTimeline(newStartDate, config.days);
  },
  { immediate: true }
);

</script>