<template>
  <div>
    <h1>All WFH Requests</h1>

    <label for="status">Status:</label>
    <select v-model="selectedStatus" @change="applyFilter">
      <option value="">All</option>
      <option value="approved">Approved</option>
      <option value="pending">Pending</option>
      <option value="rejected">Rejected</option>
    </select>

    <div v-if="filteredRequests.length > 0">
      <ul>
        <li v-for="request in filteredRequests" :key="request.Request_ID">
          <p><strong>Request ID:</strong> {{ request.Request_ID }}</p>
          <p><strong>Staff Name:</strong> {{ request.Staff_Name }}</p>
          <p><strong>Department:</strong> {{ request.Staff_Department }}</p>
          <p><strong>Position:</strong> {{ request.Staff_Position }}</p>
          <p><strong>Start Date:</strong> {{ request.Start_Date }}</p>
          <p><strong>End Date:</strong> {{ request.End_Date }}</p>
          <p><strong>Time:</strong> {{ request.Time }}</p>
          <p><strong>Request Type:</strong> {{ request.Request_Type }}</p>
          <p><strong>Status:</strong> {{ request.Status }}</p>
          <p><strong>Application Date:</strong> {{ request.Application_Date }}</p>
          <p><strong>Approver:</strong> {{ request.Approver }}</p>
          <p><strong>Reason:</strong> {{ request.Reason }}</p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No requests found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedStatus: '',  // Holds the value selected in the dropdown
      allRequests: [],     // All WFH requests fetched from the API
      filteredRequests: [],  // The filtered WFH requests
    };
  },
  methods: {
    applyFilter() {
      // Filter the WFH requests based on the selected status
      if (this.selectedStatus === '') {
        // If no status is selected (i.e., "All"), show all requests
        this.filteredRequests = this.allRequests;
      } else {
        // Filter requests by the selected status
        this.filteredRequests = this.allRequests.filter(
          request => request.Status && request.Status.toLowerCase() === this.selectedStatus.toLowerCase()
        );
      }
      console.log('Filtered Requests:', this.filteredRequests);
    },
    fetchRequests() {
      // Fetch WFH requests using Axios
      axios.get('http://localhost:5000/api/wfh/requests')
        .then(response => {
          this.allRequests = response.data;
          this.filteredRequests = response.data;  // Initially show all requests
          console.log('All Requests:', response.data);

          // Apply filter once data is fetched
          this.applyFilter();
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
  },
  mounted() {
    // Fetch requests when the component is mounted
    this.fetchRequests();
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>