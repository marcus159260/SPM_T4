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
        <table v-if="approvedRequests.length > 0" class="table align-middle mt-10 bg-white">
            <thead class="bg-light">
                <tr>
                    <th>Request_ID</th>
                    <th>Name & Staff_ID</th>
                    <th>Department & Position</th>
                    <th>Request_Type / Time of WFH requested days</th>
                    <th>Application_Date</th>
                    <th>WFH_Start_Date</th>
                    <th>Reason of Application</th>
                    <th>Status</th>
                    <th>Withdrawal_Reason</th>
                </tr>
            </thead>
            <tbody v-for="staff in approvedRequests" :key="staff.Staff_ID">
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
                        <p class="mb-1">{{ staff.Reason }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Status }}</p>
                    </td>
                    <td>
                        <p class="mb-1">{{ staff.Withdrawal_Reason }}</p>
                    </td>
                </tr>
            </tbody>
        </table>
        <div v-if="approvedRequests.length === 0" class="text-center mt-3">
            <p>No Approved requests.</p>
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
            managerId: null
        };
    },
    methods: {
        get_manager_details(managerId) {
            axios.get(`http://127.0.0.1:5000//api/users/get-manager/${managerId}`)
                .then(response => {
                    this.managerDetails = response.data.data; // Store manager details
                })
                .catch(error => {
                    console.error("Error fetching manager details:", error);
                });
        },
        fetchRequests() {
            // Fetch WFH requests using Axios
            axios.get(`http://127.0.0.1:5000//api/wfh/requests?managerId=${this.managerId}`)

                .then(response => {
                    this.allRequests = response.data;
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
        approvedRequests() {
            // Filter for approved requests
            return this.allRequests.filter(request =>
                request.Status === 'Approved' &&
                request.Approver_ID === this.managerId
            );
        }
    },
    mounted() {
        // Fetch requests when the component is mounted
        this.managerId = this.authStore.user.staff_id || null;
        console.log(this.managerId)
        this.get_manager_details(this.managerId);
        this.fetchRequests();

    },

};
</script>

<style scoped>
/* Add your styles here */
#pending-header span {
    color: green;
}
</style>