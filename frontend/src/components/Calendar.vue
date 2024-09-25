<template>
    <div class="wrap">
        <h2>{{ title }}</h2>
        <div class="left">
            <DayPilotNavigator id="nav" :config="navigatorConfig" ref="navigator" />
        </div>
        <div class="content">
            <DayPilotCalendar id="calendar" :config="calendarConfig" ref="calendar" />
        </div>
    </div>
</template>
  
<script>
import { ref, onMounted, reactive } from 'vue';
import { DayPilot, DayPilotCalendar, DayPilotNavigator } from '@daypilot/daypilot-lite-vue';

export default {
name: 'Calendar',
components: {
    DayPilotCalendar,
    DayPilotNavigator
},
props: {
    title: {
    type: String,
    default: 'My Personal Schedule'
    },
    days: {
    type: Array,
    default: () => []
    }
},
setup() {
    const calendar = ref(null);
    const navigator = ref(null);

    const navigatorConfig = {
      showMonths: 3,
      skipMonths: 3,
      selectMode: "Day",
      startDate: DayPilot.Date.today(),
      selectionDay: "2024-31-12",
      onTimeRangeSelected: args => {
        calendarConfig.startDate = args.day;
      }
    };

    const calendarConfig = ref({
        viewType: "Resources",  // View type set to resources for team scheduling
        durationBarVisible: true,  
        startDate: DayPilot.Date.today(),
        businessBeginsHour: 9,  
        businessEndsHour: 19, 
        // headerDateFormat: "ddd d MMM",  
        timeRangeSelectedHandling: "Enabled",
        onTimeRangeSelected: async (args) => {
            await createEvent(args.start, args.end, args.resource);
            calendar.value.control.clearSelection();
        },
        onEventClick: (args) => {
            editEvent(args.e);
        },
        eventDeleteHandling: "Enabled",
        onEventDelete: (args) => {
            deleteEvent(args.e);
        },
        onEventMoved: (args) => {
            console.log("Event moved", args.e);
        },
        onEventResized: (args) => {
            console.log("Event resized", args.e);
        },
    });

    const createEvent = async (start, end, resource) => {
    const form = [
        {name: "Text", id: "text"},
        {name: "Start", id: "start", type: "datetime", disabled: true},
        {name: "End", id: "end", type: "datetime", disabled: true},
        {name: "Resource", id: "resource", type: "select", options: calendar.value.control.columns.list}
    ];
    const data = {
        start,
        end,
        resource,
        id: DayPilot.guid()
    };
    const modal = await DayPilot.Modal.form(form, data);
    if (modal.canceled) {
        return;
    }

    const e = modal.result;
    calendar.value.control.events.add(e);
    };

    const editEvent = async (e) => {
        const form = [
            {name: "Text", id: "text"},
            {name: "Start", id: "start", type: "datetime", disabled: true},
            {name: "End", id: "end", type: "datetime", disabled: true},
            {name: "Resource", id: "resource", type: "select", options: calendar.value.control.columns.list}
        ];
        const data = e.data;
        const modal = await DayPilot.Modal.form(form, data);
        if (modal.canceled) {
            return;
        }

        calendar.value.control.events.update(modal.result);
    };

    const deleteEvent = async(e) => {
      const modal = await DayPilot.Modal.confirm("Do you really want to delete this event?");
      if (modal.canceled) {
        return;
      }
      calendar.value.control.events.remove(e);
    };

    const loadEvents = () => {
    const events = [
        // does not work yet
        {
        id: "e1",
        start: DayPilot.Date.today().addHours(8),
        end: DayPilot.Date.today().addHours(12),
        type: "event",
        text: "WFH (Morning)",
        barColor: "#6aa84f"  // Green for WFH
        },
        {
        id: "e2",
        start: DayPilot.Date.today().addHours(13),
        end: DayPilot.Date.today().addHours(16),
        type: "event",
        text: "WFO (Afternoon)",
        barColor: "#1155cc"  // Blue for WFO
        },

    ];
    calendar.value.control.update({events});
    navigator.value.control.update({events});
    };

    const loadResources = () => {
    const columns = [
        {name: "John", id: "John"},
        {name: "Alice", id: "Alice"},
        {name: "Muhammad", id: "Muhammad"},
        {name: "Victor", id: "Victor"},
        {name: "Rachel", id: "Rachel"},
    ];
    calendar.value.control.update({columns});
    navigator.value.control.update({columns});
    };

    onMounted(() => {
        loadEvents();
        loadResources();
    });

    return {
    navigatorConfig,
    calendarConfig,
    calendar,
    navigator,
    loadEvents,
    loadResources,
    editEvent,
    createEvent
    };
}
};
</script>

<style>
.wrap {
    display: flex;
}

.left {
    margin-right: 10px;
}

.content {
    flex-grow: 1;
}

.navigator_default_busy.navigator_default_cell {
    border-bottom: 4px solid #ee4f2ecc;
    box-sizing: border-box;
}
</style>
  