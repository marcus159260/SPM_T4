<template>
  <div>
    <CalendarNavigation
      :currentDate="startDate"
      :earliestDate="earliestDate"
      :latestDate="latestDate"
      @dateChanged="onDateChanged"
    />
    <hrCalendar
      :resources="resources"
      :events="events"
      :startDate="startDate"
      :days="days"
    />
  </div>
</template>

<script>
import hrCalendar from '../components/hrCalendar.vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { DayPilot } from 'daypilot-pro-vue';
import CalendarNavigation from '../components/CalendarNavigation.vue';

export default {
  components: {
    hrCalendar,
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
      departmentCounts: [],
      earliestDate: startOfWeek.addDays(-60),
      latestDate: startOfWeek.addDays(90),
    };
  },

  mounted() {
    Promise.all([this.loadResources(), this.loadEvents(), this.loadDepartmentCounts()])
    .then(() => {
      this.updateDepartmentNames();
    });
  },

  methods: {

    async loadEvents() {
      const params = {
        startDate: this.startDate.toString(),
        days: this.days,
      };
      return axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/all_events`, {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
        params: params,
      }).then((response) => {
        this.events = response.data;
      }).catch((error) => {
        console.error('Error fetching events:', error);
      });
    },

    async loadResources() {
      return axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/users/resources`, {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
      }).then((response) => {
        this.resources = response.data;
      }).catch((error) => {
        console.error('Error fetching requests:', error);
      });
    },

    async loadDepartmentCounts() {
      const params = {
        start_date: this.startDate.toString('yyyy-MM-dd'),
        end_date: this.startDate.addDays(this.days - 1).toString('yyyy-MM-dd'),
      };
      return axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/users/department_counts`, {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
        params: params,
      }).then((response) => {
        this.departmentCounts = response.data;
        // console.log('Department counts:', this.departmentCounts);
      }).catch((error) => {
        console.error('Error fetching department counts:', error);
      });
    },

    updateDepartmentNames() {
      // Create a mapping from department name to counts
      const countsMap = {};
      this.departmentCounts.forEach(dept => {
        countsMap[dept.department] = {
          wfhCount: dept.wfh_count,
          wfoCount: dept.wfo_count,
        };
      });

      // Update department names in resources
      this.resources.forEach(department => {
        const deptName = department.name.split(' (')[0]; // Remove existing counts
        const counts = countsMap[deptName];
        if (counts) {
          department.name = `${deptName} (WFH: ${counts.wfhCount}, WFO: ${counts.wfoCount})`;
        } else {
          console.warn(`No counts found for department: ${deptName}`);
        }
      });
    },

    onDateChanged(newStartDate) {
      this.startDate = newStartDate;
      Promise.all([this.loadEvents(), this.loadDepartmentCounts()])
      .then(() => {
        this.updateDepartmentNames();
      });
    },

  }

};
</script>