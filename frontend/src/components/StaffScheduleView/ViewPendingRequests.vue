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
                        <th scope="col">Cancel Request</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in filteredRequests" :key="request.Request_ID">
                        <th scope="row">{{ request.Request_ID }}</th>
                        <td>{{ request.Request_Type }}</td>
                        <td>
                            <span class="badge rounded-pill text-bg-warning">{{ request.Status }}</span>
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
                        <td>
                            <button @click="openCancelModal(request)">Cancel</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <p>No pending requests available within the date range.</p>
        </div>

        <!-- Cancel Modal -->
        <div v-if="showCancelModal" class="modal">
            <div class="modal-content">
                <h4>Cancel Request</h4>
                <!-- <p v-if="isRecurringRequest">Select the date to cancel for the recurring request:</p>
                <ul v-if="isRecurringRequest">
                    <li v-for="date in selectedRequest.Requested_Date" :key="date">
                        <input
                            type="radio"
                            v-model="selectedDateToCancel"
                            :value="date"
                            name="cancel-date"
                        />
                        {{ formatDate(date) }}
                    </li>
                </ul> -->

                <p>Reason for cancellation:</p>
                <textarea v-model="cancellationReason"></textarea>

                <div class="modal-actions">
                    <button 
                        :disabled="!canSubmitCancellation()" 
                        @click="confirmCancellation"
                        :class="['confirm-button', { 'disabled-button': !canSubmitCancellation() }]">
                        Confirm
                    </button>

                    <button @click="closeCancelModal">Close</button>
                </div>
            </div>
        </div>

        <!-- Success Modal -->
        <div v-if="showSuccessModal" class="modal">
            <div class="modal-content">
                <h4>Cancellation Successful</h4>
                <p>Your request has been successfully cancelled.</p>
                <div class="modal-actions">
                    <button @click="closeSuccessModal">Close</button>
                </div>
            </div>
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
            requestsData: [],
            showCancelModal: false, // Track modal visibility
            showSuccessModal: false, // Track success modal visibility
            selectedRequest: null, // Track the selected request
            selectedDateToCancel: null, // For selecting a single date to cancel
            cancellationReason: "", // Capture the reason
            isRecurringRequest: false, // Track if the request is recurring
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

        openCancelModal(request) {
            this.selectedRequest = request;
            // this.isRecurringRequest = request.Request_Type === "RECURRING";
            // this.selectedDateToCancel = null; // Reset selected date
            this.cancellationReason = "";
            this.showCancelModal = true;
        },

        closeCancelModal() {
            this.showCancelModal = false;
        },

        async confirmCancellation() {
            if (!this.cancellationReason) {
                // Optionally handle this case without an alert, such as highlighting the input
                return;
            }

            // if (this.isRecurringRequest && !this.selectedDateToCancel) {
            //     // Optionally handle this case without an alert
            //     return;
            // }

            axios.post('http://127.0.0.1:5000/api/wfh/requests/cancel', {
                    Request_ID: this.selectedRequest.Request_ID,
                    Withdrawal_Reason: this.cancellationReason,
                    dateToCancel: this.selectedDateToCancel,
                    Staff_id: this.staffId
                }).then((response) => {
                    this.showCancelModal = false;
                    this.showSuccessModal = true;
                    this.withdrawalReason = '';
                    this.fetchRequests(); // Refresh the list
                }).catch((error) => {
                    console.error('Error cancelling pending request:', error);
                    alert('An error occurred while cancelling the pending request.');
                }
            );
        },

        closeSuccessModal() {
            this.showSuccessModal = false; // Close the success modal
        },

        canSubmitCancellation() {
            // if (this.isRecurringRequest) {
            //     // For recurring requests, both the date and reason are required
            //     return this.selectedDateToCancel && this.cancellationReason.trim().length > 0;
            // } else {
                // For adhoc requests, only the cancellation reason is required
                return this.cancellationReason.trim().length > 0;
            }
        // }
    },
    mounted() {
        this.fetchRequests();
    }
};
</script>

<style scoped>
.content-wrapper {
    padding-left: 20px;
}

.modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    max-width: 500px;
    width: 100%;
}

.modal-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

/* Confirm button styles */
.confirm-button {
    background-color: #007bff; /* Bootstrap primary color */
    color: white; /* White text */
    border: none; /* No border */
    padding: 10px 20px; /* Add padding */
    border-radius: 5px; /* Rounded corners */
    cursor: pointer; /* Pointer cursor */
    transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
}

.confirm-button:hover:not(.disabled-button) {
    background-color: #0056b3; /* Darker shade on hover */
    transform: translateY(-2px); /* Slight lift effect on hover */
}

.confirm-button:focus {
    outline: none; /* Remove default focus outline */
    box-shadow: 0 0 0 4px rgba(0, 123, 255, 0.5); /* Custom focus outline */
}

/* Disabled state for the confirm button */
.disabled-button {
    background-color: #ccc;
    color: #666;
    cursor: not-allowed;
    border: 1px solid #aaa;
}
</style>