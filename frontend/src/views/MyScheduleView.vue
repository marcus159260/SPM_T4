<template>
    <div>
      <myCalendar
        :title="'My Schedule'"
      />
    </div>
  </template>
  
  <script>
  import myCalendar from '../components/myCalendar.vue';
  // import apiService from '../services/apiService';
  
  export default {
    components: {
      myCalendar,
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
  