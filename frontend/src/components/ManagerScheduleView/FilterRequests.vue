<template>
  <div class="content-wrapper">
    <h2 class="mt-4">All WFH Requests</h2>

    <div class="filter-container mb-3">
      <label for="statusFilter" class="status-label">Status</label>
      <select id="statusFilter" v-model="selectedStatus" class="status-dropdown">
        <option value="">All</option>
        <option value="Approved">Approved</option>
        <option value="Pending">Pending</option>
        <option value="Rejected">Rejected</option>
        <option value="Withdrawn">Withdrawn</option>
      </select>
    </div>

    <div v-if="filteredRequests.length > 0">
      <table class="table">
        <thead>
          <tr>
            <th scope="col">Request ID</th>
            <th scope="col">Staff Name</th>
            <th scope="col">Department</th>
            <th scope="col">Position</th>
            <th scope="col">Status</th>
            <th scope="col">Start Date</th>
            <th scope="col">End Date</th>
            <th scope="col">Time</th>
            <th scope="col">Request Type</th>
            <th scope="col">Request Reason</th>
            <th scope="col">Application Date</th>
            <th scope="col">Approver</th>
            <th scope="col">Rejection Reason</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="request in filteredRequests" :key="request.Request_ID">
            <th scope="row">{{ request.Request_ID }}</th>
            <td>{{ request.Staff_Name }}</td>
            <td>{{ request.Staff_Department }}</td>
            <td>{{ request.Staff_Position }}</td>
            <td>
              <span :class="{
                  'badge rounded-pill text-bg-success': request.Status === 'Approved',
                  'badge rounded-pill text-bg-warning': request.Status === 'Pending',
                  'badge rounded-pill text-bg-danger': request.Status === 'Rejected',
                  'badge rounded-pill text-bg-secondary': request.Status === 'Withdrawn'
              }">{{ request.Status }}</span>
            </td>
            <td>{{ formatDate(request.Start_Date) }}</td>
            <td>{{ formatDate(request.End_Date) }}</td>
            <td>{{ request.Time }}</td>
            <td>{{ request.Request_Type }}</td>
            <td>{{ request.Reason }}</td>
            <td>{{ formatDate(request.Application_Date) }}</td>
            <td>{{ request.Approver }}</td>
            <td>{{ request.Rejection_Reason }}</td>
          </tr>
        </tbody>
      </table>
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
    },
    fetchRequests() {
      // Fetch WFH requests using Axios
      axios.get('http://127.0.0.1:5000/api/wfh/requests')
        .then(response => {
          this.allRequests = response.data;
          this.filteredRequests = response.data;  // Initially show all requests
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const year = date.getFullYear();
      return `${day}-${month}-${year}`; // Format to DD-MM-YYYY
    },
  },
  watch: {
    // Watch for changes in the selectedStatus and apply the filter
    selectedStatus() {
      this.applyFilter();
    }
  },
  mounted() {
    // Fetch requests when the component is mounted
    this.fetchRequests();
  },
};
</script>


<style>
  .filter-container {
    display: flex;
    align-items: center;
    gap: 10px; /* Adds space between label and dropdown */
  }

  .status-label {
    font-weight: bold;
    margin-left: 25px;
    margin-right: 10px;
  }

  .status-dropdown {
    padding: 3px;
    font-size: 14px;
  }

  /* Increase the row height */
  tr {
    height: 80px;
  }

  td, th {
    vertical-align: middle; /* Center content vertically in rows */
    padding: 15px; /* Add more padding for increased row size */
    text-align: center;
  }

  h2 {
    padding:8px;
    font-weight: bolder;
  }
</style>