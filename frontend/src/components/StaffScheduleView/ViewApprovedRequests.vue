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
                        <th scope="col">Requested Date(s)</th>
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
                            <span class="badge rounded-pill text-bg-success">{{ request.Status }}</span>
                        </td>
                        <td>
                            <ul>
                                <li v-for="date in request.Requested_Date" :key="date">
                                {{ formatDate(date) }}
                                </li>
                            </ul>
                        </td>
                        <td>{{ request.Time }}</td>
                        <td>{{ request.Reason }}</td>
                        <td>{{ formatDate(request.Application_Date) }}</td>
                        <td>{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                        <td><button @click="attemptWithdrawal(request)">Withdraw</button></td>
                    </tr>
                </tbody>
            </table>
            <div v-if="showWithdrawalModal" class="modal">
                <div class="modal-content">
                    <span class="close" @click="cancelWithdrawal">&times;</span>
                    <h3>Withdraw WFH Request</h3>
                    <p>Please provide a reason for withdrawal:</p>
                    <textarea v-model="withdrawalReason"></textarea>
                    <div class="modal-actions">
                    <button @click="confirmWithdrawal">Confirm</button>
                    <button @click="cancelWithdrawal">Cancel</button>
                    </div>
                </div>
            </div>

            <div v-if="showWithdrawalSuccessfulMessage" class="withdrawal-success-message">
                <p>Your WFH request has been withdrawn successfully.</p>
                <button @click="closeWithdrawalSuccessfulMessage">Close</button>
            </div>
        </div>
        <div v-else>
            <p>No approved requests available within the date range.</p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: "StaffRequests",
    data() {
        return {
            selectedStatus: "Approved", // Default filter is Approved
            staffId: 150076,
            requestsData: [],
            showWithdrawalModal: false,
            withdrawalReason: '',
            showWithdrawalSuccessfulMessage: false,
        };
    },
    computed: {
        filteredRequests() {
            const currentDate = new Date();
            const minus60Days = new Date(currentDate);
            minus60Days.setDate(currentDate.getDate() - 60); // 60 days ago

            const plus90Days = new Date(currentDate);
            plus90Days.setDate(currentDate.getDate() + 90); // 90 days forward

            // Filter requests for 'Approved' status and within date range
            return this.requestsData.filter((request) => {
                const endDate = new Date(request.End_Date);
                return (
                    request.Status === "Approved" &&
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
        },

        attemptWithdrawal(request) {
            // Check if the request is within 2 weeks backward and forward
            const today = new Date();
            const startDate = new Date(request.Start_Date);
            const endDate = new Date(request.End_Date);
            const twoWeeksAgo = new Date();
            const twoWeeksLater = new Date();
            twoWeeksAgo.setDate(today.getDate() - 14);
            twoWeeksLater.setDate(today.getDate() + 14);

            if ((startDate >= twoWeeksAgo && startDate <= twoWeeksLater) ||(endDate >= twoWeeksAgo && endDate <= twoWeeksLater)) {
                this.selectedRequest = request;
                this.showWithdrawalModal = true;
            } else {
                alert('You can only withdraw requests within 2 weeks backward and forward.');
            }
        },

        confirmWithdrawal() {
            if (!this.withdrawalReason.trim()) {
                alert('Please provide a reason for withdrawal.');
                return;
            }
            axios.post('http://127.0.0.1:5000/api/wfh/requests/withdraw', {
                Request_ID: this.selectedRequest.Request_ID,
                Rejection_Reason: this.withdrawalReason,
                Staff_ID: this.staffId
            }).then((response) => {
                this.showWithdrawalModal = false;
                this.showWithdrawalSuccessfulMessage = true;
                this.withdrawalReason = '';
                this.fetchRequests(); // Refresh the list
            }).catch((error) => {
                console.error('Error withdrawing request:', error);
                alert('An error occurred while withdrawing the request.');
            });
        },

        cancelWithdrawal() {
            this.showWithdrawalModal = false;
            this.withdrawalReason = '';
        },

        closeWithdrawalSuccessfulMessage() {
            this.showWithdrawalSuccessfulMessage = false;
        },

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

.modal {
  display: block; 
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  width: 50%;
  border-radius: 5px;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  cursor: pointer;
}

.modal-actions {
  margin-top: 15px;
}

.modal-actions button {
  margin-right: 10px;
}

.withdrawal-success-message {
  background-color: #dff0d8;
  color: #3c763d;
  padding: 15px;
  margin-top: 20px;
  border-radius: 5px;
}

</style>