<template>
    <div>
        <div class="row">
            <div class="col-12">
                <h6 id="pending-header" v-if="managerDetails" class="mt-10">
                    Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
                    Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
                    Department: <span>{{ managerDetails.Department }}</span> <br />
                    Position: <span>{{ managerDetails.Position }}</span> <br />
                    <!-- In charge of: <br>
          &emsp;Dept -> <span>{{ managerDetails.Department }}</span> <br>
          &emsp;Position -> <span>{{ managerDetails.Position }}</span> -->
                </h6>
            </div>
        </div>

        <button @click="fetchRequests" class="btn btn-primary mt-3">Refresh Requests</button>

        <div class="table-responsive">
            <table v-if="rejectedRequests.length > 0" class="table table-striped align-middle mt-10 bg-white">
                <thead class="bg-light">
                    <tr>
                        <th scope="col">Request ID</th>
                        <th scope="col">Staff Name</th>
                        <th scope="col">Department</th>
                        <th scope="col">Position</th>
                        <th scope="col">Status</th>
                        <th scope="col" class="date-column">Requested Date</th>
                        <th scope="col">Time</th>
                        <th scope="col">Request Type</th>
                        <th scope="col">Request Reason</th>
                        <th scope="col" class="date-column">Application Date</th>
                        <th scope="col">Rejection Reason</th>
                        <th scope="col">Withdrawal Reason</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="staff in rejectedRequests" :key="staff.Staff_ID">
                        <th scope="row">{{ staff.Request_ID }}</th>
                        <td>{{ staff.Staff_Name }}</td>
                        <td>{{ staff.Staff_Department }}</td>
                        <td>{{ staff.Staff_Position }}</td>
                        <td>
                            <span :class="{
                                'badge rounded-pill text-bg-success': staff.Status === 'Approved',
                                'badge rounded-pill text-bg-warning': staff.Status === 'Pending'|| staff.Status === 'Withdrawn - Pending',
                                'badge rounded-pill text-bg-danger': staff.Status === 'Rejected',
                                'badge rounded-pill text-bg-secondary': staff.Status === 'Withdrawn'
                            }">{{ staff.Status }}</span>
                        </td>
                        <td>{{ formatDate(staff.Start_Date) }}</td>
                        <td>{{ staff.Time }}</td>
                        <td>{{ staff.Request_Type }}</td>
                        <td>{{ staff.Reason }}</td>
                        <td>{{ formatDate(staff.Application_Date) }}</td>
                        <td>{{ staff.Rejection_Reason }}</td>
                        <td>{{ staff.Withdrawal_Reason }}</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div v-if="rejectedRequests.length === 0" class="text-center mt-3">
            <p>No Rejected requests.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { useAuthStore } from '../../stores/auth';


export default {
    data() {
        return {
            allRequests: [], // Holds the data fetched from the API
            managerDetails: [],
            // managerId: null,
            // refreshInterval: null
        };
    },
    props: {
        managerId: {
            type: Number,
            required: true
        },
        role: {
            type: Number,
            required: true
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
        get_manager_details() {
            axios.get(`http://127.0.0.1:5000/api/users/get-manager/${this.managerId}`)
                .then(response => {
                    this.managerDetails = response.data.data; // Store manager details
                })
                .catch(error => {
                    console.error("Error fetching manager details:", error);
                });
        },
        fetchRequests() {
            // Fetch WFH requests using Axios
            axios.get(`http://127.0.0.1:5000/api/wfh/requests?managerId=${this.managerId}`)

                .then(response => {
                    this.allRequests = response.data;
                    // console.log(this.allRequests)
                })
                .catch(error => {
                    console.error('Error fetching requests:', error);
                });
        },

    },
    computed: {
        authStore() {
            return useAuthStore(); // Access the auth store
        },
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
        // console.log(this.managerId);
        // console.log(this.role);
        this.fetchRequests();
        // this.managerId = this.authStore.user.staff_id || null;
        this.get_manager_details();
    },

};
</script>

<style scoped>
/* Add your styles here */
#pending-header span {
    color: green;
}

.date-column {
    min-width: 120px;
    /* Adjust width as needed */
}
</style>