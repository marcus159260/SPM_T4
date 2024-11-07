<template>
  <div class="content-wrapper">
    <div v-if="requestsData?.length > 0">
      <h2 class="mt-5">{{ requestsData[0].Staff_Name }}</h2>

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

      <div class="table-responsive">
        <table class="table table-striped table-bordered align-middle mt-3">
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
              <td data-cell="request ID">{{ request.Request_ID }}</td>
              <td data-cell="request type">{{ request.Request_Type }}</td>
              <td data-cell="status">
                <span :class="{
                  'badge rounded-pill text-bg-success': request.Status === 'Approved',
                  'badge rounded-pill text-bg-warning': request.Status === 'Pending' || request.Status === 'Withdrawn - Pending',
                  'badge rounded-pill text-bg-danger': request.Status === 'Rejected',
                  'badge rounded-pill text-bg-secondary': request.Status === 'Withdrawn'
                }">{{ request.Status }}</span>
              </td>
              <td data-cell="requested date">{{ formatDate(request.Start_Date) }}</td>
              <td data-cell="time">{{ request.Time }}</td>
              <td data-cell="reason">{{ request.Reason }}</td>
              <td data-cell="application date">{{ formatDate(request.Application_Date) }}</td>
              <td data-cell="approver">{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
              <td data-cell="rejection reason">{{ request.Rejection_Reason }}</td>
              <td data-cell="withdrawal reason">{{ request.Withdrawal_Reason }}</td>
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
import { useAuthStore } from "../../stores/auth";

export default {
  name: "StaffRequests",
  data() {
    return {
      staff_fname: "",
      staff_lname: "",
      selectedStatus: "",
      approverName: "",
      requestsData: []
    }
  },
  props: {
    staffId: {
      type: Number,
      required: true
    },
    role: {
      type: Number,
      required: true
    }
  },
  computed: {
    filteredRequests() {
      if (Array.isArray(this.requestsData) && this.selectedStatus) {
        return this.requestsData.filter(
          (request) => request.Status.includes(this.selectedStatus)
        );
      }
      return this.requestsData;
    },
    authStore() {
      return useAuthStore();
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
        const response = await axios.get(`http://127.0.0.1:5000/api/wfh/requests/${this.staffId}`,
          {
            headers: {
              'X-Staff-ID': this.staffId,
              'X-Staff-Role': this.role,
            },
          }
        );
        if (response.data) {
          this.requestsData = response.data
        }
        else {
          console.log("No data found for this staff ID");
        }
      } catch (error) {
        console.error("Error fetching requests:", error);
      }
    }
  },

  mounted() {
    // console.log(this.staffId);
    // console.log(this.role);
    this.fetchRequests();
  }


}
</script>

<style>
@media (max-width: 400px) {
  .table-responsive {
    max-width: 100%;
    /* Increase this value to make the container wider */
    margin: 0 auto;
    /* Center the table container */
  }

  th {
    display: none;
  }

  td {
    display: grid;
    gap: 0.5rem;
    grid-template-columns: 20ch auto;
  }

  td:first-child {
    padding-top: 2rem;
  }

  td:last-child {
    padding-top: 2rem;
  }

  td::before {
    content: attr(data-cell) ": ";
    font-weight: 700;
    text-transform: capitalize;
  }
}
</style>
<!-- <style>
.filter-container {
  display: flex;
  align-items: center;
  gap: 10px; /* space between label and dropdown */
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

.table-responsive {
overflow-x: auto; /* Makes table scrollable on small screens */
} 

</style> -->
<style>
@import '../style.css';
</style>