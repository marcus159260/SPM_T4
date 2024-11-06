<template>
  <div class="content-wrapper">
    <h6 id="pending-header" v-if="managerDetails" class="mt-10">
      Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
      Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
      Department: <span>{{ managerDetails.Department }}</span> <br />
      Position: <span>{{ managerDetails.Position }}</span> <br />
    </h6>

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
      <div class="table-responsive">
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Request ID</th>
              <th scope="col">Staff Name</th>
              <th scope="col">Department</th>
              <th scope="col">Position</th>
              <th scope="col">Status</th>
              <th scope="col">Requested Date</th>
              <th scope="col">Time</th>
              <th scope="col">Request Type</th>
              <th scope="col">Request Reason</th>
              <th scope="col">Application Date</th>
              <th scope="col">Rejection Reason</th>
              <th scope="col">Withdrawal Reason</th>
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
                    'badge rounded-pill text-bg-warning': request.Status === 'Pending'|| request.Status === 'Withdrawn - Pending',
                    'badge rounded-pill text-bg-danger': request.Status === 'Rejected',
                    'badge rounded-pill text-bg-secondary': request.Status === 'Withdrawn'
                }">{{ request.Status }}</span>
              </td>
              <td>{{ formatDate(request.Start_Date) }}</td>
              <td>{{ request.Time }}</td>
              <td>{{ request.Request_Type }}</td>
              <td>{{ request.Reason }}</td>
              <td>{{ formatDate(request.Application_Date) }}</td>
              <td>{{ request.Rejection_Reason }}</td>
              <td>{{ request.Withdrawal_Reason }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div v-else>
      <p>No requests.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export default {
  data() {
    return {
      selectedStatus: '', // Holds the value selected in the dropdown
      approver_id: null, // Set this to the name you want to filter by
      allRequests: [], // All WFH requests fetched from the API
      filteredRequests: [], // The filtered WFH requests
      managerDetails: [],
    };
  },
  computed: {
    authStore() {
            return useAuthStore(); // Access the auth store
        },
  },
  methods: {
    applyFilter() {
      const today = new Date();

      // Calculate two months back and three months ahead
      const twoMonthsBack = new Date(today);
      const threeMonthsAhead = new Date(today);

      // Adjust for date range (no change here)
      twoMonthsBack.setDate(today.getDate() - 61);
      threeMonthsAhead.setDate(today.getDate() + 91);

      // Remove the time component for accurate date comparison
      twoMonthsBack.setHours(0, 0, 0, 0);
      threeMonthsAhead.setHours(0, 0, 0, 0);

      // Filter the WFH requests
      this.filteredRequests = this.allRequests.filter(request => {
        const requestStartDate = new Date(request.Start_Date);

        // Remove the time component from requestStartDate
        requestStartDate.setHours(0, 0, 0, 0);

        // Compare dates without time affecting the result
        const isWithinDateRange = requestStartDate >= twoMonthsBack && requestStartDate <= threeMonthsAhead;

        // Check if the request matches the selected status, include "Withdrawn - Pending" under "Pending"
        const matchesStatus = this.selectedStatus === '' || 
                              (request.Status && (
                                request.Status.toLowerCase() === this.selectedStatus.toLowerCase() || 
                                (this.selectedStatus.toLowerCase() === 'pending' && request.Status.toLowerCase() === 'withdrawn - pending')
                              ));

        return isWithinDateRange && matchesStatus;
      });
    },

    get_manager_details(approver_id) {
      axios.get(`http://127.0.0.1:5000/api/users/get-manager/${approver_id}`)
        .then(response => {
          this.managerDetails = response.data.data; // Store manager details
        })
        .catch(error => {
          console.error("Error fetching manager details:", error);
        });
    },
    
    fetchRequests() {
      axios.get(`http://127.0.0.1:5000/api/wfh/requests/approver/${this.approver_id}`, {
        headers: {
          'X-Staff-ID': this.authStore.user.staff_id,
          'X-Staff-Role': this.authStore.user.role,
        },
      })
        .then(response => {
          if (response.data.length > 0 && response.data[0].Error) {
            // If there is an error in the response, display the error message
            alert(response.data[0].Error);
            this.allRequests = [];  // Clear the request list
          } else {
            this.allRequests = response.data;
          }
          this.applyFilter();  // Apply filters after fetching the requests
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
    selectedStatus() {
      this.applyFilter(); // Re-apply filter whenever status changes
    }
  },
  mounted() {
    this.approver_id = this.authStore.user.staff_id || null;
    console.log(this.approver_id) 
    this.get_manager_details(this.approver_id);
    this.fetchRequests(); // Fetch requests when component is mounted

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
    margin-left: 15px;
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
    margin-left: 8px;
  }

  p{
    font-weight: bold;
    margin-left: 15px;
  }

  #pending-header span {
  color: green;
}
</style>