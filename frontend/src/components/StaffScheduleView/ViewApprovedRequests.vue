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
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="request in filteredRequests" :key="request.Request_ID">
                        <th scope="row">{{ request.Request_ID }}</th>
                        <td>{{ request.Request_Type}}</td>
                        <td>
                            <span class="badge rounded-pill text-bg-success">{{ request.Status }}</span>
                        </td>
                        <td>{{ formatDate(request.Start_Date) }}</td>
                        <td>{{ request.Time }}</td>
                        <td>{{ request.Reason }}</td>
                        <td>{{ formatDate(request.Application_Date) }}</td>
                        <td>{{ request.Approver_FName }} {{ request.Approver_LName }}</td>
                        <td><button @click="attemptWithdrawal(request)">Withdraw</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <p>No approved requests available within the date range.</p>
        </div>
        <div>
            <PopupWrapper id='popup' class="flex-container justify-content-center" :visible="isPopupVisible"
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

export default {
    name: "StaffRequests",
    data() {
        return {
            selectedStatus: "Approved", // Default filter is Approved
            staffId: 150076,
            requestsData: [],
            withdrawalReason: '',
            showSuccessModal: false,
            isPopupVisible: false,
            selectedRequestId: null
        };
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

            const twoWeeksAgo = new Date(startDate);
            twoWeeksAgo.setDate(twoWeeksAgo.getDate() - 14);            
            const twoWeeksLater = new Date(endDate);
            twoWeeksLater.setDate(twoWeeksLater.getDate() + 14);

            if (today >= twoWeeksAgo && today <= twoWeeksLater) {
                this.selectedRequest = request;
                this.isPopupVisible = true; 
                document.getElementById('popup').style.display = 'flex';
                document.getElementById('popup').style.border = '1px black solid';
            } else {
                document.getElementById('errormsg').innerHTML = `You can only withdraw requests within 2 weeks backward and forward.<br>`;                
                // alert('You can only withdraw requests within 2 weeks backward and forward.');

            }
        },

        confirmWithdrawal() {
            if (!this.withdrawalReason.trim()) {
                console.log('error from popup: no error msg');
                document.getElementById('errormsg').innerHTML = `Reason cannot be empty<br>`;                
                return;
            }
            axios.post('http://127.0.0.1:5000/api/wfh/requests/withdraw', {
                Request_ID: this.selectedRequest.Request_ID,
                Withdrawal_Reason: this.withdrawalReason,
                Staff_ID: this.staffId
            }).then((response) => {
                this.isPopupVisible = false;
                document.getElementById('popup').style.border = '';
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