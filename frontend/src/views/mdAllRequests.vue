<template>
    <div>
      <h2>WFH Requests</h2>
      <ul>
        <li v-if="loadingRequests">Loading WFH requests...</li>
        <li v-for="request in wfhRequests" :key="request.id">
          {{ request.name }} - {{ request.status }}
        </li>
      </ul>

    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        wfhRequests: [],
        userProfiles: [],
        loadingRequests: true,
        loadingProfiles: true,
      };
    },
    async created() {
      await this.fetchWFHRequests();
    },
    methods: {
      async fetchWFHRequests() {
        try {
          const response = await fetch('http://localhost:5000/api/wfh/requests');
          const data = await response.json();
          this.wfhRequests = data;
        } catch (err) {
          console.error('Error fetching WFH requests:', err);
        } finally {
          this.loadingRequests = false;
        }
      },
  //     async fetchUserProfiles() {
  //       try {
  //         const response = await fetch('http://localhost:5000/api/wfh/user-profiles');
  //         const data = await response.json();
  //         this.userProfiles = data;
  //       } catch (err) {
  //         console.error('Error fetching user profiles:', err);
  //       } finally {
  //         this.loadingProfiles = false;
  //       }
  //     },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  
