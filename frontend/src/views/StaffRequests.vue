<template>
    <div>
        <h6 class="mt-5">Name: {{ staff_fname }} {{staff_lname}}</h6>

        <div class="filter-container mb-3">
            <label for="statusFilter">Filter by Status</label>
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
            <th scope="col">Time</th>
            <th scope="col">Reason</th>
            <th scope="col">Application Date</th>
            <th scope="col">Approver</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="request in filteredRequests" :key="request.request_id">
                <th scope="row">{{ request.request_id }}</th>
                <td>{{ request.request_type}}</td>
                <td>
                    <span :class="{
                        'badge rounded-pill text-bg-success': request.status === 'Approved',
                        'badge rounded-pill text-bg-warning': request.status === 'Pending',
                        'badge rounded-pill text-bg-danger': request.status === 'Rejected',
                        'badge rounded-pill text-bg-light': request.status === 'Withdrawn'
                    }">{{ request.status}}</span></td>
                <td>{{ formatDate(request.start_date) }}</td>
                <td>{{ formatDate(request.end_date) }}</td>
                <td>{{ request.time }}</td>
                <td>{{ request.reason }}</td>
                <td>{{ formatDate(request.application_date) }}</td>
                <td>{{ request.approver_fname }} {{request.approver_lname }}</td>
            </tr>
        </tbody>
        </table>
        <p>{{ filteredRequests }}</p>
    </div>
</template>

<script>
import axios from 'axios';
// import { mapState } from 'vuex'; // If you're using Vuex to manage the logged-in user state

export default {
    name: "StaffRequests",
    data(){
        return{
            staff_fname: "",
            staff_lname: "",
            selectedStatus: "",
            staffId: null,
            requestsData : []
        }
    },
    computed: {
    filteredRequests() {
      if (this.selectedStatus) {
        return this.requestsData.filter(request => request.status === this.selectedStatus);
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