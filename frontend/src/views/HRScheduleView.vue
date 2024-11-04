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
      axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/all_events`, {
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
      axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/users/resources`, {
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
