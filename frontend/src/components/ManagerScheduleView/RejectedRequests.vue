<template>
    <div>
        <div class="row">
            <div class="col-12">
                <h6 id="pending-header" v-if="managerDetails" class="mt-10">
                    Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
                    Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
                    Department: <span>{{ managerDetails.Department }}</span> <br />
                    Position: <span>{{ managerDetails.Position }}</span> <br />
                </h6>
            </div>
        </div>

        <button @click="fetchRequests" class="btn btn-primary mt-3">Refresh Requests</button>

        <!-- Apply table-responsive conditionally based on the number of requests -->
        <div :class="{'table-responsive': filteredRequests.length > 0}">
            <table v-if="filteredRequests.length > 0" class="table table-striped table-bordered align-middle mt-3">
                <thead>
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
                    <tr v-for="staff in filteredRequests" :key="staff.Staff_ID">
                        <td data-cell="request ID">{{ staff.Request_ID }}</td>
                        <td data-cell="staff name">{{ staff.Staff_Name }}</td>
                        <td data-cell="department">{{ staff.Staff_Department }}</td>
                        <td data-cell="position">{{ staff.Staff_Position }}</td>
                        <td data-cell="status" class="table-cell">
                            <span :class="{
                                'badge rounded-pill text-bg-success': staff.Status === 'Approved',
                                'badge rounded-pill text-bg-warning': staff.Status === 'Pending'|| staff.Status === 'Withdrawn - Pending',
                                'badge rounded-pill text-bg-danger': staff.Status === 'Rejected',
                                'badge rounded-pill text-bg-secondary': staff.Status === 'Withdrawn'
                            }">{{ staff.Status }}</span>
                        </td>
                        <td data-cell="requested date">{{ formatDate(staff.Start_Date) }}</td>
                        <td data-cell="time">{{ staff.Time }}</td>
                        <td data-cell="request type">{{ staff.Request_Type }}</td>
                        <td data-cell="request reason">{{ staff.Reason }}</td>
                        <td data-cell="application date">{{ formatDate(staff.Application_Date) }}</td>
                        <td data-cell="rejection reason">{{ staff.Rejection_Reason }}</td>
                        <td data-cell="withdrawal reason">{{ staff.Withdrawal_Reason }}</td>
                    </tr>
                </tbody>
            </table>
            <!-- Message when no requests are available -->
            <div v-if="filteredRequests.length === 0" class="text-center mt-3">
                <p>No Rejected Requests.</p>
            </div>
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
            filteredRequests: [],
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
    computed: {
            authStore() {
                return useAuthStore(); // Access the auth store
            },
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
            axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/users/get-manager/${this.managerId}`)
                .then(response => {
                    this.managerDetails = response.data.data; // Store manager details
                })
                .catch(error => {
                    console.error("Error fetching manager details:", error);
                });
        },
        applyFilter() {
            const today = new Date();

            // Calculate two months back and three months ahead
            const twoMonthsBack = new Date(today);
            const threeMonthsAhead = new Date(today);

            // Adjust for date range
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

                // Check if the request status is 'Approved'
                const matchesStatus = request.Status === 'Rejected';

                return isWithinDateRange && matchesStatus;
            });
        },
        fetchRequests() {
            axios.get(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/approver/${this.managerId}`, {
                headers: {
                'X-Staff-ID': this.managerId,
                'X-Staff-Role': this.role,
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