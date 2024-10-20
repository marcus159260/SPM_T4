<template>
  <div>
    <teamCalendar
      :title="'My Team Schedule'"
      :resources="resources"
    />
  </div>
</template>

<script>
import teamCalendar from '../components/StaffScheduleView/teamCalendar.vue';
import axios from 'axios';
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
      Staff_ID: 140894 //hardcode team manager
      
    };
  },
  mounted() {
    // var url = "http://127.0.0.1:5000/api/users/by-team-employees/" + config.reporting_manager;
    // axios
    //   .get(url)
    //   .then((response) => {
    //     this.resources = response.data;
    //     console.log("Loaded resources:", this.resources);
    //   })
    //   .catch((error) => {
    //     console.error('Error fetching requests:', error);
    //   });
  },
  
};


</script>
