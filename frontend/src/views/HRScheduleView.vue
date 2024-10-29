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
import { useAuthStore } from '@/stores/auth';

export default {
  components: {
    hrCalendar,
  },

  computed: {
    authStore() {
      return useAuthStore();
    },
  },

  data() {
    return {
      employees: [],
      resources: [],
      events: []
    };
  },

  mounted() {
    this.loadResources();
    this.loadEvents();
  },

  methods: {
    loadEvents() {
      axios.get('http://127.0.0.1:5000/api/wfh/all_events', {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
      }).then((response) => {
        this.events = response.data;
      }).catch((error) => {
        console.error('Error fetching events:', error);
      });
    },
    loadResources() {
      axios.get('http://127.0.0.1:5000/api/users/resources', {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
      }).then((response) => {
        this.resources = response.data;
      }).catch((error) => {
        console.error('Error fetching requests:', error);
      });
    }
  }

};
</script>
