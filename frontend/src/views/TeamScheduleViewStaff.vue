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
  import teamCalendar from '../components/StaffScheduleView/teamCalendar.vue';
  import { useAuthStore } from '@/stores/auth';
  
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
        Staff_ID: useAuthStore().user.staff_id

        
      };
    }
    
  };
  
  
  </script>
