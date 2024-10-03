<template>
    <div class="content-wrapper">
    <div v-if="requests.length > 0">
        <h2>Your Requests</h2>
        <h3 class="mt-5">{{ requests[0].Staff_Name }}</h3>

        <div class="filter-container mb-3">
            <label for="statusFilter">Status</label>
            <select id="statusFilter" v-model="selectedStatus">
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
                    <th scope="col">Start Date</th>
                    <th scope="col">End Date</th>
                    <th scope="col">Reason</th>
                    <th scope="col">Application Date</th>
                    <th scope="col">Approver</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in filteredRequests" :key="request.Request_ID">
                    <th scope="row">{{ request.Request_ID }}</th>
                    <td>{{ request.Request_Type }}</td>
                    <td>
                        <span :class="{
                            'badge rounded-pill text-bg-success': request.Status === 'Approved',
                            'badge rounded-pill text-bg-warning': request.Status === 'Pending',
                            'badge rounded-pill text-bg-danger': request.Status === 'Rejected',
                            'badge rounded-pill text-bg-light': request.Status === 'Withdrawn'
                        }">
                            {{ request.Status }}
                        </span>
                    </td>
                    <td>{{ formatDate(request.Start_Date) }}</td>
                    <td>{{ formatDate(request.End_Date) }}</td>
                    <td>{{ request.Reason }}</td>
                    <td>{{ formatDate(request.Application_Date) }}</td>
                    <td>{{ request.Approver }}</td>       
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
      <p>No requests available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
    name: "StaffRequests",
    data(){
        return{
            // test
            requests: [],
            selectedStatus: "",
        }
    },
    mounted() {
    // Fetch the requests data when the component is mounted
    axios
      .get('http://127.0.0.1:5000/api/wfh/requests')
      .then((response) => {
        this.requests = response.data;
      })
      .catch((error) => {
        console.error('Error fetching requests:', error);
      });
  },
    computed: {
    filteredRequests() {
      if (this.selectedStatus) {
        return this.requests.filter(request => request.Status === this.selectedStatus);
      }
      return this.requests;
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
            const staffId = this.$route.params.staffId || 140929; 
            const response = await axios.get(`http://localhost:5000/api/requests/${staffId}`);
            console.log("API Response:", response.data);
            if (response.data.length > 0) {
                this.requestsData = response.data;
                console.log("requestsData:", this.requestsData);
                // Assuming that all requests have the same staff_fname and staff_lname
                this.staff_fname = this.requestsData[0].staff_fname;
                this.staff_lname = this.requestsData[0].staff_lname;
            } else {
            console.log("No data found for this staff ID");
            }
        } catch (error) {
        console.error("Error fetching requests:", error);
      }
        }
    },
    mounted() {
    this.fetchRequests();
    const staffId = this.$route.params.staff_id; // Get the staff_id from the route

    // Fetch data from backend
    axios.get(`http://localhost:5000/api/requests/${staffId}`)
      .then(response => {
        this.requestsData = response.data; // Store the API response in requestsData
        console.log(response.data); // Log the data for debugging
      })
      .catch(error => {
        console.error('Error fetching data:', error); // Handle any errors
      });
  }


}
</script>

<style>
    .content-wrapper {
        padding-left: 20px;
    }
</style>
