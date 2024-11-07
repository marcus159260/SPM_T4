<template>
  <div class="scheduler-container">
    <DayPilotScheduler :config="config" ref="schedulerRef" />
  </div>
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, watch, defineProps, defineEmits, onMounted } from 'vue';

const props = defineProps({
  resources: {
    type: Array,
    required: true,
  },
  events: {
    type: Array,
    required: true,
  },
  startDate: {
    type: Object, 
    required: true,
  },
  days: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['dateChanged']);

const config = reactive({
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
  scale: "Manual",
  cellDuration: 720,
  days: props.days,
  startDate: props.startDate,
  timeRangeSelectedHandling: "Disabled",
  eventClickHandling: "Disabled",
  treeEnabled: true,
  resources: [],
  events: [],
  cellWidthSpec: "Auto",
  heightSpec: "Full",
  width: "100%"
});
const schedulerRef = ref(null);

const today = DayPilot.Date.today();
const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
const daysToMonday = currentDayOfWeek - 1; // Subtract to get back to Monday
const startOfWeek = today.addDays(-daysToMonday);

config.startDate = startOfWeek;

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
      start: date + "T14:00:00",
      end: date + "T18:00:00",
      label: "PM",
    });
  }
  return timeline;
}

config.timeline = generateTimeline(config.startDate, config.days);

const updateConfigForScreenSize = () => {
  if (window.innerWidth < 768) {
    config.cellWidthSpec = "Fixed";
    config.cellWidth = 50;
  } else {
    config.cellWidthSpec = "Auto";
  }
};

onMounted(() => {
  updateConfigForScreenSize();
  window.addEventListener('resize', updateConfigForScreenSize);
});

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
  () => [props.startDate, props.days],
  ([newStartDate, newDays]) => {
    config.startDate = newStartDate;
    config.days = newDays;
    config.timeline = generateTimeline(newStartDate, newDays);
  }
);

</script>

<style scoped>

.scheduler-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

</style>