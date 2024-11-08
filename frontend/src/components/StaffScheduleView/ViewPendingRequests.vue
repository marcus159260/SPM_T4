<template>
    <div class="content-wrapper">
        <div v-if="filteredRequests?.length > 0">
            <h2 class="mt-5">{{ requestsData[0].Staff_Name }}</h2>
            <div class="table-responsive">
                <table class="table table-striped table-bordered align-middle mt-3">
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
                            <th scope="col" class="fixed-column">Cancel Request</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in filteredRequests" :key="request.Request_ID">
                            <td data-cell="request ID">{{ request.Request_ID }}</td>
                            <td data-cell="request type">{{ request.Request_Type }}</td>
                            <td data-cell="status">
                                <span class="badge rounded-pill text-bg-warning">{{ request.Status }}</span>
                            </td>
                            <td data-cell="requested date">{{ formatDate(request.Start_Date) }}</td>
                            <td data-cell="time">{{ request.Time }}</td>
                            <td data-cell="reason">{{ request.Reason }}</td>
                            <td data-cell="application date">{{ formatDate(request.Application_Date) }}</td>
                            <td data-cell="approver">{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                            <td data-cell="withdrawal reason">{{ request.Withdrawal_Reason }}</td>
                            <td data-cell="cancel request" class="fixed-column">
                                <button v-if="request.Status === 'Pending'"
                                    @click="openCancelModal(request.Request_ID)">Cancel</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <p>No pending requests available within the date range.</p>
        </div>

        <!-- Cancel Modal -->
        <div v-if="isPopupVisible">
            <PopupWrapper id="cancelPopup" class="flex-container justify-content-center" :visible="isPopupVisible"
                @update:visible="isPopupVisible = $event">
                <template #content>
                    <div class="justify-content-center">
                        <h3 class="my-4" style="color:black">Reason for Rejection</h3>
                        <form>
                            <textarea style="width:400px; height:150px" class="form-control"
                                v-model="cancellationReason" placeholder="Enter reason for cancellation"></textarea>
                            <div class="d-flex flex-column my-2">
                                <p id="errormsg" class="text-danger mx-0"></p>
                                <button type="button" class="btn btn-primary"
                                    @click="confirmCancellation(selectedRequestId)">Submit</button>
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
import { useAuthStore } from "../../stores/auth";

export default {
    name: "StaffRequests",
    data() {
        return {
            requestsData: [],
            showSuccessModal: false, // Track success modal visibility
            selectedRequest: null, // Track the selected request
            cancellationReason: "", // Capture the reason
            isPopupVisible: false, // Popup visibility
            selectedRequestid: null,
        };
    },

    props: {
        staffId: {
            type: Number,
            required: true
        },
        role: {
            type: Number,
            required: true
        }
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
                    (request.Status === "Pending" || request.Status === "Withdrawn - Pending") &&
                    endDate >= minus61Days &&
                    endDate <= plus91Days
                );
            });
        },
        authStore() {
            return useAuthStore();
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
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/${this.staffId}`,
                    {
                        headers: {
                            'X-Staff-ID': this.staffId,
                            'X-Staff-Role': this.role,
                        },
                    }
                );
                if (response.data) {
                    this.requestsData = response.data;
                    console.log(this.requestsData);
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
            // document.getElementById('cancelPopup').style.display = 'flex';
            // document.getElementById('cancelPopup').style.border = '1px black solid';
        },

        async confirmCancellation(selectedRequestId) {
            axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/cancel`, {
                Request_ID: selectedRequestId,
                Withdrawal_Reason: this.cancellationReason,
                Staff_id: this.staffId
            })

                .then(response => {
                    if (response) {
                        this.fetchRequests();
                        this.isPopupVisible = false; // Hide the popup after submission
                        // document.getElementById('cancelPopup').style.border = '';
                        this.openSuccessModal();
                    }
                })
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
        // console.log(this.staffId);
        // console.log(this.role);
        this.fetchRequests();
    }
};
</script>

<style scoped>
@import '../style.css';

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

/* Popup wrapper styling */
.flex-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1002;
    /* Ensure it's above other content */
    display: flex;
    justify-content: center;
    align-items: center;
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