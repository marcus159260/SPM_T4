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
import { DayPilot } from 'daypilot-pro-vue';

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
      events: [],
      startDate: DayPilot.Date.today(),
      departmentCounts: []
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
      return axios.get('http://127.0.0.1:5000/api/wfh/all_events', {
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

    async loadResources() {
      return axios.get('http://127.0.0.1:5000/api/users/resources', {
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
      return axios.get('http://127.0.0.1:5000/api/users/department_counts', {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
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
        const deptName = department.name;
        const counts = countsMap[deptName];
        if (counts) {
          department.name = `${deptName} (WFH: ${counts.wfhCount}, WFO: ${counts.wfoCount})`;
        } else {
          console.warn(`No counts found for department: ${deptName}`);
        }
      });
    },


  }

};
</script>
