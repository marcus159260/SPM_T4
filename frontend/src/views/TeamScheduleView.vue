<template>
    <div>
      <Calendar :title="'My Team Schedule'" />
    </div>
  </template>
  
  <script>
  import Calendar from '../components/Calendar.vue';
  
  export default {
    components: {
      Calendar
    },
  };
  </script>
  