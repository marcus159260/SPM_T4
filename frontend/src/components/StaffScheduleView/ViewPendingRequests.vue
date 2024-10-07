<template>
    <div class="content-wrapper">
        <div v-if="filteredRequests?.length > 0">
            <h3 class="mt-5">{{ requestsData[0].Staff_Name }}</h3>

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
                    <tr v-for="request in filteredRequests" :key="request.Request_ID">
                        <th scope="row">{{ request.Request_ID }}</th>
                        <td>{{ request.Request_Type}}</td>
                        <td>
                            <span class="badge rounded-pill text-bg-warning">{{ request.Status }}</span>
                        </td>
                        <td>{{ formatDate(request.Start_Date) }}</td>
                        <td>{{ formatDate(request.End_Date) }}</td>
                        <td>{{ request.Time }}</td>
                        <td>{{ request.Reason }}</td>
                        <td>{{ formatDate(request.Application_Date) }}</td>
                        <td>{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <p>No pending requests available within the date range.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "StaffRequests",
    data() {
        return {
            selectedStatus: "Pending", 
            staffId: 150076,
            requestsData: []
        };
    },
    computed: {
        filteredRequests() {
            const currentDate = new Date();
            const minus60Days = new Date(currentDate);
            minus60Days.setDate(currentDate.getDate() - 60); // 60 days ago

            const plus90Days = new Date(currentDate);
            plus90Days.setDate(currentDate.getDate() + 90); // 90 days forward

            return this.requestsData.filter((request) => {
                const endDate = new Date(request.End_Date);
                return (
                    request.Status === "Pending" &&
                    endDate >= minus60Days &&
                    endDate <= plus90Days
                );
            });
        }
    },
    methods: {
        formatDate(dateString) {
            const date = new Date(dateString);
            const day = String(date.getDate()).padStart(2, "0");
            const month = String(date.getMonth() + 1).padStart(2, "0"); // Months are zero-based
            const year = date.getFullYear();
            return `${day}-${month}-${year}`; // Format to DD-MM-YYYY
        },
        async fetchRequests() {
            try {
                // Get staffId from route params (if using Vue Router) or from a state
                const staffId = this.$route.params.staffId || 150076;
                const response = await axios.get(
                    `http://127.0.0.1:5000/api/wfh/requests/${staffId}`
                );
                if (response.data) {
                    this.requestsData = response.data;
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
    }
};
</script>

<style>
.content-wrapper {
    padding-left: 20px;
}
</style>