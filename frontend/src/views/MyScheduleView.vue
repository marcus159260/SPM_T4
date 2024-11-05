<template>
  <div>
    <CalendarNavigation
      :currentDate="startDate"
      :earliestDate="earliestDate"
      :latestDate="latestDate"
      @dateChanged="onDateChanged"
    />
    <myCalendar
      :events="events"
      :resources="resources"
      :startDate="startDate"
      :days="days"
    />
  </div>
</template>

<script>
import myCalendar from '../components/myCalendar.vue';
import axios from 'axios';
import { DayPilot } from 'daypilot-pro-vue';
import { useAuthStore } from '@/stores/auth';
import CalendarNavigation from '../components/CalendarNavigation.vue';

export default {
  components: {
    myCalendar,
    CalendarNavigation
  },
  computed: {
    authStore() {
      return useAuthStore();
    },
  },
  data() {
    const today = DayPilot.Date.today();
    const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
    const daysToMonday = currentDayOfWeek - 1;
    const startOfWeek = today.addDays(-daysToMonday);
    return {
      resources: [],
      events: [],
      startDate: DayPilot.Date.today(),
      days: 7,
      earliestDate: startOfWeek.addDays(-60),
      latestDate: startOfWeek.addDays(90),
    };
  },

  mounted() {
    this.loadResources();
    this.loadEvents();
  },

  methods: {
    loadResources() {
      var url = `${import.meta.env.VITE_API_BASE_URL}/api/users/` + this.authStore.user.staff_id;
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

    loadEvents() {
      var url = `${import.meta.env.VITE_API_BASE_URL}/api/wfh/events/` + this.authStore.user.staff_id;
      axios.get(url).then((response) => {
        this.events = response.data;
      }).catch((error) => {
        console.error('Error fetching events:', error);
      });
    },

    onDateChanged(newStartDate) {
      this.startDate = newStartDate;
      this.loadEvents();
    },
  }

};
</script>
