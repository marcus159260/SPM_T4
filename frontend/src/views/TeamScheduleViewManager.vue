<template>
    <div>
      <teamCalendar
        :title="'My Team Schedule'"
        :resources="resources"
        @dateChanged="onDateChanged"
      />
    </div>
  </template>

<script>
import teamCalendar from '../components/teamCalendarManager.vue';

export default {
  components: {
    teamCalendar,
  },
  data() {
    return {
      teamEvents: [],
      teamResources: [],
      employees:[],
      resources:[],
      
    };
  },
  
  
};


</script>
