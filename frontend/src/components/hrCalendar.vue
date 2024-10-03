<template>
  <DayPilotScheduler :config="config" ref="schedulerRef" />
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, onMounted } from 'vue';

const config = reactive({
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
  scale: "CellDuration",
  cellDuration: 720,
  days: DayPilot.Date.today().daysInMonth(),
  startDate: DayPilot.Date.today().firstDayOfMonth(),
  timeRangeSelectedHandling: "Disabled",

  eventClickHandling: "Disabled",
  treeEnabled: true,
});
const schedulerRef = ref(null);

const loadEvents = () => {
  const events = [
    { id: 1, start: "2024-10-01T00:00:00", end: "2024-10-05T00:00:00", text: "WFH", resource: "R1" },
    { id: 2, start: DayPilot.Date.today(), end: DayPilot.Date.today().addDays(5), text: "WFO", resource: "R2" }
  ];
  config.events = events;
};

const loadResources = () => {
  const resources = [
    {
      "name": "Engineering",
      "id": "D1",
      "expanded": true,
      children: [
        {
          "name": "130002",
          "id": "T1",
          "expanded": true,
          children: [
            {
              "name": "Alice",
              "id": "P1"
            },
            {
              "name": "John",
              "id": "P2"
            },
          ]
        },
        {
          "name": "140894",
          "id": "T2",
          "expanded": true,
          children: [
            {
              "name": "Peter",
              "id": "P3"
            },
            {
              "name": "Ali",
              "id": "P4"
            },
          ]
        },
      ]
    },
    {
      "name": "Sales",
      "id": "D2",
      "expanded": true,
      children: [
        {
          "name": "140008",
          "id": "T3",
          "expanded": true,
          children: [
            {
              "name": "Rachel",
              "id": "P5"
            }
          ]
        }
      ]
    }
  ];
  config.resources = resources;
};

onMounted(() => {
  loadResources();
  loadEvents();
});
</script>
