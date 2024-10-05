<template>
  <div>
    <hrCalendar
      :title="'HR Schedule'"
      :resources="resources"
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
      allEvents: [],
      employees: [],
      resources: []
    };
  },
  // async created() {
  //   try {
  //     const response = await apiService.getAllEmployeesNames();
  //     console.log('Employees data:', response.data);

  //     this.employees = response.data.map((employee) => ({
  //       name: employee.Full_Name,
  //       id: employee.Staff_ID.toString(),
  //     }));
  //     console.log('Formatted employees:', this.employees);
  //   } catch (error) {
  //     console.error('Error fetching employees:', error);
  //   }

  // },
  mounted() {
    axios
      .get('http://127.0.0.1:5000/api/users/resources')
      .then((response) => {
        this.resources = response.data;
        console.log("Loaded resources:", this.resources);
      })
      .catch((error) => {
        console.error('Error fetching requests:', error);
      });
  },
};
</script>
