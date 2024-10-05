//NOT IN USE
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
    },
    // events: [],
    // resources: []
    events: {
        type: Array,
        default: () => [],
    },
    employees: {
        type: Array,
        default: () => [],
    },
    role: {
        type: String,
        required: true, // 'staff', 'manager', 'hr'
    },
},
setup(props) {
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

    const calendarConfig = reactive({
        viewType: "Resources",  // View type set to resources for team scheduling
        durationBarVisible: true,  
        startDate: DayPilot.Date.today(),
        businessBeginsHour: 9,  
        businessEndsHour: 19, 
        // timeRangeSelectedHandling: props.role === 'staff' ? 'Disabled' : 'Enabled',
        timeRangeSelectedHandling: "Enabled",
    });

    const loadResources = () => {
        // const columns = [
        //     {name: "John", id: "John"},
        //     {name: "Alice", id: "Alice"},
        //     {name: "Muhammad", id: "Muhammad"},
        //     {name: "Victor", id: "Victor"},
        //     {name: "Rachel", id: "Rachel"},
        // ];
        calendar.value.control.update({columns: props.employees});
        navigator.value.control.update({columns: props.employees});
    };

    const loadEvents = () => {
    //   const events = [
        // {
        //   id: 1,
        //   start: "2024-09-28T10:00:00",
        //   end: "2024-09-28T11:00:00",
        //   resource: "John",
        //   text: "Event 1",
        //   barColor: "#6aa84f",
        // },
    //     {
    //       id: 2,
    //       start: "2024-09-30T13:00:00",
    //       end: "2024-09-30T16:00:00",
    //       resource: "John",
    //       text: "Event 2",
    //       barColor: "#f1c232",
    //     },
    //     {
    //       id: 3,
    //       start: "2024-09-30T13:30:00",
    //       end: "2024-09-30T16:30:00",
    //       resource: "Alice",
    //       text: "Event 3",
    //       barColor: "#cc4125",
    //     }
    //   ];
      calendar.value.control.update({events: props.events});
      navigator.value.control.update({events: props.events});
    };

    onMounted(() => {
        loadResources();
        loadEvents()
    });

    return {
    navigatorConfig,
    calendarConfig,
    calendar,
    navigator,
    loadResources,
    loadEvents
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
  