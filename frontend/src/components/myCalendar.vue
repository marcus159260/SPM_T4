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
    // onTimeRangeSelected: async (args) => {
    //   const scheduler = args.control;
    //   const modal = await DayPilot.Modal.prompt("Create a new event:", "Event 1");
    //   scheduler.clearSelection();
    //   if (modal.canceled) { return; }
    //   scheduler.events.add({
    //     start: args.start,
    //     end: args.end,
    //     id: DayPilot.guid(),
    //     resource: args.resource,
    //     text: modal.result
    //   });
    // },
    eventClickHandling: "Disabled",
    eventHoverHandling: "Bubble",
    bubble: new DayPilot.Bubble({
      onLoad: (args) => {
        // if the event object doesn't specify "bubbleHtml" property
        // this onLoad handler will be called to provide the bubble HTML
        args.html = "Event details";
      }
    }),
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
            "name": "John",
            "id": "R1"
        }
    ];
    config.resources = resources;
  };
  
  onMounted(() => {
    loadResources();
    loadEvents();
  });
  </script>
  