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
                            <th scope="col">Withdraw Request</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in filteredRequests" :key="request.Request_ID">
                            <td data-cell="request ID">{{ request.Request_ID }}</td>
                            <td data-cell="request type">{{ request.Request_Type }}</td>
                            <td data-cell="status">
                                <span class="badge rounded-pill text-bg-success">{{ request.Status }}</span>
                            </td>
                            <td data-cell="requested date">{{ formatDate(request.Start_Date) }}</td>
                            <td data-cell="time">{{ request.Time }}</td>
                            <td data-cell="reason">{{ request.Reason }}</td>
                            <td data-cell="application date">{{ formatDate(request.Application_Date) }}</td>
                            <td data-cell="approver">{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                            <td data-cell="withdraw"><button @click="attemptWithdrawal(request)">Withdraw</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
        <div v-else>
            <p>No approved requests available within the date range.</p>
        </div>
        <div>
            <PopupWrapper id='withdrawalPopup' class="flex-container justify-content-center pop" :visible="isPopupVisible"
                @update:visible="isPopupVisible = $event">
                <template #content>
                <div width="100%" class="justify-content-center">
                    <h3 class="my-4" style="color:black">Reason for Withdrawal</h3>
                    <form>
                    <textarea style='width:400px;height:150px' class="form-control" v-model="withdrawalReason"
                        placeholder="Enter reason for withdrawal"></textarea>
                    <div class="d-flex flex-column my-2">
                        <p id="errormsg" class="text-danger mx-0"></p>
                        <button type="button" class="btn btn-primary" @click="confirmWithdrawal">Submit</button>
                    </div>
                    </form>
                </div>
                </template>
            </PopupWrapper>
        </div>

        <!-- Withdrawal Success Modal -->
        <div v-if="showSuccessModal" class="modal">
            <div class="modal-content">
                <h4>Withdrawal Successful</h4>
                <p>Your request has been successfully withdrawn.</p>
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
            selectedStatus: "Approved", // Default filter is Approved
            requestsData: [],
            withdrawalReason: '',
            showSuccessModal: false,
            isPopupVisible: false,
            selectedRequestId: null
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
    components: {
        PopupWrapper
    },
    computed: {
        filteredRequests() {
            const currentDate = new Date();
            const minus61Days = new Date(currentDate);
            minus61Days.setDate(currentDate.getDate() - 61); 

            const plus91Days = new Date(currentDate);
            plus91Days.setDate(currentDate.getDate() + 91); 

            // Filter requests for 'Approved' status and within date range
            return this.requestsData.filter((request) => {
                const endDate = new Date(request.End_Date);
                return (
                    request.Status === "Approved" &&
                    endDate >= minus61Days &&
                    endDate <= plus91Days
                );
            });
        },
        authStore() {
            return useAuthStore();
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
                // const staffId = this.$route.params.staffId || 150076;
                const response = await axios.get(
                    `${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/${this.staffId}`,
                    {
                        headers: {
                            'X-Staff-ID': this.staffId,
                            'X-Staff-Role': this.role,
                        }
                    }
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

            const twoWeeksAgo = new Date(startDate);
            twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);            
            const twoWeeksLater = new Date(endDate);
            twoWeeksLater.setDate(twoWeeksLater.getDate() + 14);

            if (today >= twoWeeksAgo && today <= twoWeeksLater) {
                this.selectedRequest = request;
                this.isPopupVisible = true; 
                document.getElementById('withdrawalPopup').style.display = 'flex';
                document.getElementById('withdrawalPopup').style.border = '1px black solid';
            } else {
                // document.getElementById('errormsg').innerHTML = `You can only withdraw requests within 2 weeks backward and forward.<br>`;                
                alert('You can only withdraw requests within 2 weeks backward and forward.');

            }
        },

        confirmWithdrawal() {
            if (!this.withdrawalReason.trim()) {
                console.log('error from popup: no error msg');
                // document.getElementById('errormsg').innerHTML = `Reason cannot be empty<br>`;                
                return;
            }
            axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/withdraw`, {
                Request_ID: this.selectedRequest.Request_ID,
                Rejection_Reason: this.withdrawalReason,
                Staff_ID: this.staffId
            }).then((response) => {
                this.isPopupVisible = false;
                document.getElementById('withdrawalPopup').style.border = '';
                this.showSuccessModal = true;
                this.fetchRequests();
            }).catch((error) => {
                console.error('Error withdrawing request:', error);
                alert('An error occurred while withdrawing the request.');
            });
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

<style>
    @import '../style.css';

    .content-wrapper {
        padding-left: 20px;
    }

.modal-content {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    width: 500px;
    max-width: 100%;
    z-index: 1001;
}

    .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    cursor: pointer;
    }

.modal-actions {
    display: flex;
    justify-content: flex-end;
}

.withdrawal-success-message {
background-color: #dff0d8;
color: #3c763d;
padding: 15px;
margin-top: 20px;
border-radius: 5px;
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