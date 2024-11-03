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
import axios from 'axios';
import { DayPilot } from 'daypilot-pro-vue';
import { useAuthStore } from '@/stores/auth';
// import { getTeamEvents, getTeamResources } from '../services/apiService';

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
      startDate: DayPilot.Date.today(),

      Staff_ID: 140894 //hardcode team manager
      
    };
  },
  computed: {
    authStore() {
      return useAuthStore();
    },
  },
  methods: {
    onDateChanged(newStartDate) {
      this.startDate = newStartDate;
      this.loadEvents();
    },
  }
};

  // mounted() {
  //   var url = "http://127.0.0.1:5000/api/users/by-team-employees/" + this.Staff_ID;
  //   axios
  //     .get(url)
  //     .then((response) => {
  //       this.resources = response.data;
  //       console.log("Loaded resources:", this.resources);
  //     })
  //     .catch((error) => {
  //       console.error('Error fetching requests:', error);
  //     });
  // },
  



</script>
