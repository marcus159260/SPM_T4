<template>
    <div>
        <h6 id="pending-header" v-if="managerDetails" class="mt-10">
            Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
            Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
            Department: <span>{{ managerDetails.Department }}</span> <br />
            Position: <span>{{ managerDetails.Position }}</span> <br />
            <!-- In charge of: <br>
          &emsp;Dept -> <span>{{ managerDetails.Department }}</span> <br>
          &emsp;Position -> <span>{{ managerDetails.Position }}</span> -->
        </h6>
        <button @click="fetchRequests" class="btn btn-primary mt-3">Refresh Requests</button>
        <table v-if="rejectedRequests.length > 0" class="table align-middle mt-10 bg-white">
            <thead class="bg-light">
                <tr>
                    <th>Request_ID</th>
                    <th>Name & Staff_ID</th>
                    <th>Department & Position</th>
                    <th>Request_Type / Time of WFH requested days</th>
                    <th>Application_Date</th>
                    <th>WFH_Start_Date</th>
                    <th>Approver_ID</th>
                    <th>Rejection Reason</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody v-for="staff in rejectedRequests" :key="staff.Staff_ID">
                <tr>
                    <td>
                        <p class="mb-1">{{ staff.Request_ID }}</p>
                    </td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="ms-3">
                                <p class="fw-bold mb-1">{{ staff.Staff_Name }}</p>
                                <p class="text-muted mb-0">{{ staff.Staff_ID }}</p>
                            </div>
                        </div>
                    </td>
                    <td>
                        <div class="d-flex align-items-center">
                            <div class="ms-3">
                                <p class="fw-bold mb-1">{{ staff.Staff_Department }}</p>
                                <p class="text-muted mb-0">{{ staff.Staff_Position }}</p>
                            </div>
                        </div>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Request_Type }} / {{ staff.Time }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Application_Date }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Start_Date }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Approver_ID }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Rejection_Reason }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Status }}</p>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="rejectedRequests.length === 0" class="text-center mt-3">
            <p>No Approved requests.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    data() {
        return {
            allRequests: [], // Holds the data fetched from the API
            managerDetails: [],
            managerId: 151408,
            // refreshInterval: null
        };
    },
    methods: {
        get_manager_details(managerId) {
            axios.get(`http://127.0.0.1:5000/api/users/get-manager/${managerId}`)
                .then(response => {
                    this.managerDetails = response.data.data; // Store manager details
                })
                .catch(error => {
                    console.error("Error fetching manager details:", error);
                });
        },
        fetchRequests() {
            // Fetch WFH requests using Axios
            axios.get('http://127.0.0.1:5000/api/wfh/requests')
                .then(response => {
                    console.log(123)
                    this.allRequests = response.data;
                    console.log(this.allRequests)
                })
                .catch(error => {
                    console.error('Error fetching requests:', error);
                });
        },
        // startAutoRefresh() {
        //     // Set the refresh interval (e.g., every 30 seconds)
        //     this.refreshInterval = setInterval(() => {
        //         this.fetchRequests();  // Auto-refresh requests
        //     }, 5000); // 2 seconds
        // },
        // stopAutoRefresh() {
        //     // Clear the interval when no longer needed
        //     if (this.refreshInterval) {
        //         clearInterval(this.refreshInterval);
        //     }
        // },
    },
    computed: {
        rejectedRequests() {
            // Filter for approved requests
            return this.allRequests.filter(request => 
            request.Status === 'Rejected' && 
            request.Approver_ID === this.managerId
            );
        }
    },
    mounted() {
        // Fetch requests when the component is mounted
        this.fetchRequests();
        this.get_manager_details(this.managerId);
        // this.startAutoRefresh();
    },
    // beforeDestroy() {
    //     // Stop the auto-refresh when the component is destroyed
    //     this.stopAutoRefresh();
    // },
};
</script>

<style scoped>
/* Add your styles here */
#pending-header span {
    color: green;
}
</style>