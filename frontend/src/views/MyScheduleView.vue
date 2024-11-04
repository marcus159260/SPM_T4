<template>
  <div>
    <myCalendar
      :title="'My Schedule'"
      :events="events"
      :resources="resources"
    />
  </div>
</template>

<script>
import myCalendar from '../components/myCalendar.vue';
import axios from 'axios';

export default {
  components: {
    myCalendar,
  },
  data() {
    return {
      events: [],
      resources: [],
      // hardcoded for now
      staff_id: "150076"
    };
  },

  mounted() {
    var url = `${import.meta.env.VITE_API_BASE_URL}/api/users/` + this.staff_id;
      axios.get(url).then((response) => {
        const staffData = response.data.data;
        this.resources = [
          {
            name: `${staffData.Staff_FName} ${staffData.Staff_LName}`,
            id: `E_${staffData.Staff_ID}`,
            expanded: true,
          },
        ];
        this.loadEvents();
      }).catch((error) => {
        console.error('Error fetching staff data:', error);
      });
  },

  methods: {
    loadEvents() {
      var url = `${import.meta.env.VITE_API_BASE_URL}/api/wfh/events/` + this.staff_id;
      axios.get(url).then((response) => {
        this.events = response.data;
      }).catch((error) => {
        console.error('Error fetching events:', error);
      });
    },
  }

};
</script>
