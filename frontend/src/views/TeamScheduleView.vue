<template>
  <div>
    <teamCalendar
      :title="'My Team Schedule'"
    />
  </div>
</template>

<script>
import teamCalendar from '../components/teamCalendar.vue';
// import { getTeamEvents, getTeamResources } from '../services/apiService';

export default {
  components: {
    teamCalendar,
  },
  data() {
    return {
      teamEvents: [],
      teamResources: [],
    };
  },
  // async created() {
  //   this.teamResources = await getTeamResources();
  //   this.teamEvents = await getTeamEvents();
  // },
};
</script>
