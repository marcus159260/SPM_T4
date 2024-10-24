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
                        <th scope="col">Requested Date</th>
                        <th scope="col">Time</th>
                        <th scope="col">Reason</th>
                        <th scope="col">Application Date</th>
                        <th scope="col">Approver</th>
                        <th scope="col">Withdrawal Reason</th>
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
                        <td>{{ formatDate(request.Start_Date) }}</td>
                        <td>{{ request.Time }}</td>
                        <td>{{ request.Reason }}</td>
                        <td>{{ formatDate(request.Application_Date) }}</td>
                        <td>{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                        <td>{{ request.Withdrawal_Reason }}</td>
                        <td>
                            <button @click="openCancelModal(request.Request_ID)">Cancel</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <p>No pending requests available within the date range.</p>
        </div>

        <!-- Cancel Modal -->
        <div>
            <PopupWrapper id='popup' class="flex-container justify-content-center" :visible="isPopupVisible"
            @update:visible="isPopupVisible = $event">
                <template #content>
                    <div width="100%" class="justify-content-center">
                        <h3 class="my-4" style="color:black">Reason for Rejection</h3>
                        <form>
                            <textarea style='width:400px;height:150px' class="form-control" v-model="cancellationReason"
                                placeholder="Enter reason for cancellation"></textarea>
                            <div class="d-flex flex-column my-2">
                                <p id="errormsg" class="text-danger mx-0"></p>
                                <button type="button" class="btn btn-primary" @click="confirmCancellation(selectedRequestId)">Submit</button>
                            </div>
                        </form>
                    </div>
                </template>
            </PopupWrapper>
        </div>

        <!-- Success Modal -->
        <div v-if="showSuccessModal" class="modal-overlay">
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
import PopupWrapper from '../PopupWrapper.vue';

export default {
    name: "StaffRequests",
    data() {
        return {
            selectedStatus: "Pending", 
            staffId: 150076,
            requestsData: [],
            showSuccessModal: false, // Track success modal visibility
            selectedRequest: null, // Track the selected request
            cancellationReason: "", // Capture the reason
            isPopupVisible: false, // Popup visibility
            selectedRequestid: null,
        };
    },

    computed: {
        filteredRequests() {
            const currentDate = new Date();
            const minus61Days = new Date(currentDate);
            minus61Days.setDate(currentDate.getDate() - 61);

            const plus91Days = new Date(currentDate);
            plus91Days.setDate(currentDate.getDate() + 91);

            return this.requestsData.filter((request) => {
                const endDate = new Date(request.End_Date);
                return (
                    (request.Status === "Pending" || request.Status === "Withdrawn-pending") &&
                    endDate >= minus61Days &&
                    endDate <= plus91Days
                );
            });
        }
    },

    components: {
        PopupWrapper
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

        openCancelModal(requestId) {
            this.selectedRequestId = requestId; // Store the request ID for rejection
            this.isPopupVisible = true; // Show the popup
            document.getElementById('popup').style.display = 'flex';
            document.getElementById('popup').style.border = '1px black solid';
        },

        async confirmCancellation(selectedRequestId) {
            axios.post('http://127.0.0.1:5000/api/wfh/requests/cancel', {
                Request_ID: selectedRequestId,
                Withdrawal_Reason: this.cancellationReason,
                Staff_id: this.staffId
            })

            .then(response => {
                if (response)  {
                    this.fetchRequests();
                    this.isPopupVisible = false; // Hide the popup after submission
                    document.getElementById('popup').style.border = '';
                    this.openSuccessModal();
                }})
                .catch(error => {
                console.error('Error rejecting request:', error);
                document.getElementById('errormsg').innerHTML = `Reason cannot be empty<br>`;
                });
            },

        openSuccessModal() {
            this.showSuccessModal = true;
        },

        closeSuccessModal() {
            this.showSuccessModal = false;
        },
    },

    mounted() {
        this.fetchRequests();
    }
};
</script>

<style scoped>
/* Styles for the overlay and modal */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 500px;
    max-width: 100%;
    z-index: 1001;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
}
</style>
