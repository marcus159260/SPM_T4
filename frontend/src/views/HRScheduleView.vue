<template>
  <div>
    <hrCalendar
      :title="'HR Schedule'"
      :resources="resources"
      :events="events"
    />
  </div>
</template>

<script>
import hrCalendar from '../components/hrCalendar.vue';
import axios from 'axios';

export default {
  components: {
    hrCalendar,
  },
  data() {
    return {
      employees: [],
      resources: [],
      events: []
    };
  },

  mounted() {
    axios.get('http://127.0.0.1:5000/api/users/resources').then((response) => {
      this.resources = response.data;
      // console.log("Loaded resources:", this.resources);
      this.loadEvents();
    }).catch((error) => {
      console.error('Error fetching requests:', error);
    });
    
  },

  methods: {
    loadEvents() {
      axios
        .get('http://127.0.0.1:5000/api/wfh/all_events')
        .then((response) => {
          this.events = response.data;
          // console.log('Loaded events:', this.events);
        })
        .catch((error) => {
          console.error('Error fetching events:', error);
        });
    },
  }

};
</script>
