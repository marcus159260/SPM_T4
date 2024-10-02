<template>
  <div>
    <hrCalendar
      :title="'HR Schedule'"
    />
  </div>
</template>

<script>
import hrCalendar from '../components/hrCalendar.vue';
import apiService from '../services/apiService';

export default {
  components: {
    hrCalendar,
  },
  data() {
    return {
      allEvents: [],
      employees: [],
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
};
</script>
