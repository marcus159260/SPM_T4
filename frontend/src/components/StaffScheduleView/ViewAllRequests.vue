<template>
    <div class="content-wrapper">
      <div v-if="requestsData?.length > 0">
        <h2 class="mt-4">{{ requestsData[0].Staff_Name }}</h2>

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


      <table class="table">
      <thead>
          <tr>
          <th scope="col">Request ID</th>
          <th scope="col">Request Type</th>
          <th scope="col">Status</th>
          <th scope="col">Requested Date</th>
          <th scope="col">Time</th>
          <th scope="col">Reason</th>
          <th scope="col">Application Date</th>
          <th scope="col">Approver</th>
          <th scope="col">Rejection Reason</th>
          <th scope="col">Withdrawal Reason</th>
          </tr>
      </thead>
      <tbody>
          <tr v-for="request in filteredRequests" :key="request.Request_ID">
              <th scope="row">{{ request.Request_ID }}</th>
              <td>{{ request.Request_Type}}</td>
              <td>
                  <span :class="{
                      'badge rounded-pill text-bg-success': request.Status === 'Approved',
                      'badge rounded-pill text-bg-warning': request.Status === 'Pending',
                      'badge rounded-pill text-bg-danger': request.Status === 'Rejected',
                      'badge rounded-pill text-bg-secondary': request.Status === 'Withdrawn'
                  }">{{ request.Status}}</span></td>
              <td>{{ formatDate(request.Start_Date) }}</td>
              <td>{{ request.Time }}</td>
              <td>{{ request.Reason }}</td>
              <td>{{ formatDate(request.Application_Date) }}</td>
              <td>{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
              <td>{{ request.Rejection_Reason }}</td>
              <td>{{ request.Withdrawal_Reason }}</td>
          </tr>
      </tbody>
      </table>
        
    </div>
    <div v-else>
      <p>No requests.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "StaffRequests",
    data(){
        return{
            staff_fname: "",
            staff_lname: "",
            selectedStatus: "",
            staff_id: 150076,
            approverName: "",
            requestsData : []
        }
    },
    computed: {
      filteredRequests() {
        if (Array.isArray(this.requestsData) && this.selectedStatus) {
        return this.requestsData.filter(
          (request) => request.Status === this.selectedStatus
        );
      }
      return this.requestsData;
      }
    },
    methods: {
      formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const year = date.getFullYear();
      return `${day}-${month}-${year}`; // Format to DD-MM-YYYY
    }, 
      async fetchRequests() {
        try {
            // Get staffId from route params (if using Vue Router) or from a state
            const staffId = this.$route.params.staff_id || 150076; 
            const response = await axios.get(`http://127.0.0.1:5000/api/wfh/requests/${this.staff_id}`);
            if(response.data){
              this.requestsData = response.data
            }
            else {
            console.log("No data found for this staff ID");
            }
        } catch (error) {
        console.error("Error fetching requests:", error);
      }
    }},

    mounted() {
    this.fetchRequests();
  }


    }
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
</style>