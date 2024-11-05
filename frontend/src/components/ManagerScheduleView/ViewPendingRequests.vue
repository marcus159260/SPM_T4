<template>
  <div id="main">
    <h6 id="pending-header" v-if="managerDetails" class="mt-10">
      Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
      Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
      Department: <span>{{ managerDetails.Department }}</span> <br />
      Position: <span>{{ managerDetails.Position }}</span> <br />
    </h6>

    <button @click="fetchRequests" class="btn btn-primary mt-3">Refresh Requests</button>
    <table v-if="pendingRequests.length > 0" class="table align-middle mt-10 bg-white">
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
          <th>Approval</th>
          <th>Withdrawal_Reason</th>
        </tr>
      </thead>

      <tbody v-for="staff in pendingRequests" :key="staff.Staff_ID">
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
          <!--Approve/Reject buttons-->
          <td class="d-flex align-items-center">
            <button v-if="staff.Status == 'Withdrawn - Pending'" @click="approveWithdrawalRequest(staff.Request_ID)"
              class="icon-button mb-5" style="padding-top: 40px;">
              <img src="../../assets/checked.png" alt="Approve Withdrawal">
            </button>
            <button v-if="staff.Status == 'Pending'" @click="approveRequest(staff.Request_ID)" class="icon-button mb-5"
              style="padding-top: 40px;">
              <img src="../../assets/checked.png" alt="Approve">
            </button>


            <button @click="rejectRequestPopup(staff.Request_ID, staff.Status)" class="icon-button mb-5"
              style="padding-top: 40px;">
              <img src="../../assets/x-button.png" alt="Reject">
            </button>
          </td>
          <!--End of Approve/Reject buttons-->
          <td>
            <p class="mb-1">{{ staff.Withdrawal_Reason }}</p>
          </td>
        </tr>

      </tbody>
    </table>

    <div v-if="pendingRequests.length === 0" class="text-center mt-3">
      <p>No pending requests.</p>
    </div>

    <div>
      <PopupWrapper id='popup' class="flex-container justify-content-center" :visible="isPopupVisible"
        @update:visible="isPopupVisible = $event">
        <template #content>
          <div width="100%" class="justify-content-center">
            <h3 class="my-4" style="color:black">Reason for Rejection</h3>
            <form>
              <textarea style='width:400px;height:150px' class="form-control" v-model="rejectionReason"
                placeholder="Enter reason for rejection"></textarea>
              <div class="d-flex flex-column my-2">
                <p id="errormsg" class="text-danger mx-0"></p>
                <button v-if="selectedRequestStatus == 'Pending'" type="button" class="btn btn-primary"
                  @click="rejectRequest(selectedRequestId)">Submit</button>
                <button v-if="selectedRequestStatus == 'Withdrawn - Pending'" type="button" class="btn btn-primary"
                  @click="rejectWithdrawalRequest(selectedRequestId)">Submit</button>

              </div>
            </form>
          </div>
        </template>
      </PopupWrapper>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import PopupWrapper from '../PopupWrapper.vue';
import { useAuthStore } from '../../stores/auth';

export default {
  data() {
    return {
      allRequests: [],     // All WFH requests fetched from the API
      managerDetails: [],
      isPopupVisible: false,
      rejectionReason: '',
      withdrawalReason: '',
      selectedRequestStatus: '',
      selectedRequestId: null,
      managerId: null
    };
  },
  components: {
    PopupWrapper
  },
  computed: {
    authStore() {
      return useAuthStore(); // Access the auth store
    },
    pendingRequests() {
      // Filter by status 'Pending' and Approver_ID matching managerId
      return this.allRequests
        .filter(request => {
          const applicationDate = new Date(request.Application_Date + 'T00:00:00'); // Use Application_Date for filtering
          const startDate = new Date(request.Start_Date + 'T00:00:00'); // Use Start_Date for filtering

          //console.log("Request object:", request);

          // Calculate the date 2 months before the Application_Date
          const twoMonthsBeforeApplicationDate = new Date(applicationDate);
          twoMonthsBeforeApplicationDate.setMonth(applicationDate.getMonth() - 2);
          // console.log("twoMonthsBeforeApplicationDate: " + twoMonthsBeforeApplicationDate)

          // Calculate the date 3 months after the Application_Date
          const threeMonthsAfterApplicationDate = new Date(applicationDate);
          threeMonthsAfterApplicationDate.setMonth(applicationDate.getMonth() + 3);
          // console.log("threeMonthsAfterApplicationDate: " + threeMonthsAfterApplicationDate)


          // Check if the Start_Date is within the range of 2 months before to 3 months after the Application_Date
          const isWithinRange = (
            startDate >= twoMonthsBeforeApplicationDate &&
            startDate <= threeMonthsAfterApplicationDate
          );

          // Return true if the request is pending, matches managerId, and Start_Date is within range
          return (
            (request.Status === 'Pending' || request.Status === 'Withdrawn - Pending') &&
            request.Approver_ID === this.managerId &&
            isWithinRange
          );
        })
        .sort((a, b) => a.Request_ID - b.Request_ID); // Sort by Request_ID in ascending order
    },
  },

  methods: {
    get_manager_details(managerId) {
      axios.get(`http://127.0.0.1:5000/api/users/get-manager/${managerId}`)
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

          //auto-reject pending requests comes in here

          // console.log(this.allRequests)
        
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
    approveRequest(requestId) {
      // console.log("Request ID clicked:", requestId); 
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/approve`, { managerId: this.managerId, Request_ID: requestId, request_Status: 'Approved' })
        .then(response => {
          console.log('response.data', response.data);
          if (response.data.status != 200) {
            alert(response.data.message);
            this.fetchRequests();  // Refresh the request list
          }
        })
        .catch(error => {
          console.log(error.response)
          if (error.response && error.response.status === 400) { //A (forward)
            alert(error.response.data.error);  // Show the error message from the backend
          }
          else if (error.response && error.response.status === 409) { //B (backdated)
            const confirmation = confirm(`${error.response.data.error}\n\nDo you still want to approve this request despite the violation?`);
            if (confirmation) {
              axios.post(`http://127.0.0.1:5000/api/wfh/requests/approve`, { managerId: this.managerId, Request_ID: requestId, request_Status: 'Approved', force_approval: true })  // Adding a flag for forced approval
                .then(response => {
                  if (response.status === 200) {
                    alert(response.data.message); 
                    this.fetchRequests(); 
                  }
                })
                .catch(forceError => {
                  console.error('Error forcing approval:', forceError);
                  alert("Failed to approve request even after confirmation. Please try again.");
                });
            }
          }
          else {
            console.error('Error approving request:', error);
            alert("An unknown error occurred. Please try again.");
          }
        });
    },
    approveWithdrawalRequest(requestId) {
      // console.log("Request ID clicked:", requestId); 
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/approvewithdrawal`, { Request_ID: requestId })
        .then(response => {
          // console.log('response.data', response.data);
          console.log('approveWithdrawalRequest');
          if (response.data == 'error') {
            alert(response.data);
          }
          else {
            this.fetchRequests();
          }
        })
        .catch(error => {
          console.error('Error rejecting request:', error);
        });
    },

    rejectRequestPopup(requestId, status) {
      this.selectedRequestId = requestId; // Store the request ID for rejection
      this.selectedRequestStatus = status;
      console.log(status);
      this.isPopupVisible = true; // Show the popup
      document.getElementById('popup').style.display = 'flex';
      document.getElementById('popup').style.border = '1px black solid';
    },
    rejectRequest(requestId) {
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/reject`, { Request_ID: requestId, Rejection_Reason: this.rejectionReason, Manager_ID: this.managerId})
        .then(response => {
          console.log('response.data', response.data);
          if (response.data == 'error') {
            // console.log(response.data.error);
            console.log('error from popup: no error msg');
            document.getElementById('errormsg').innerHTML = `Reason cannot be empty.<br>`;

          }
          else {
            this.fetchRequests();
            this.isPopupVisible = false; // Hide the popup after submission
            document.getElementById('popup').style.border = '';

          }
        })
        .catch(error => {
          console.error('Error rejecting request:', error);
        });
    },
    rejectWithdrawalRequest(requestId) {
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/rejectwithdrawal`, { Request_ID: requestId, Withdrawal_Reason: this.rejectionReason })
        .then(response => {
          console.log('response.data', response.data);

            this.fetchRequests();
            this.isPopupVisible = false; // Hide the popup after submission
            document.getElementById('popup').style.border = '';
    
        })
        .catch(error => {
          console.error('Error rejecting request:', error);
          if (error.response.data.message == 'Reason cannot be empty.') {
            // console.log(response.data.error);
            console.log('error from popup: no error msg');
            document.getElementById('errormsg').innerHTML = `Reason cannot be empty.<br>`;
        }
    });
    },

  },
  mounted() {
    // Fetch requests when the component is mounted
    this.managerId = this.authStore.user.staff_id || null;
    console.log(this.managerId);

    this.fetchRequests();
    this.get_manager_details(this.managerId);
  },
};
</script>

<style scoped>
/* Add your styles here */
#pending-header span {
  color: green;
}

.icon-button {
  background: none;
  /* Remove default button background */
  border: none;
  /* Remove button border */
  padding: 0;
  /* Remove default padding */
  margin: 0 5px;
  /* Add space between buttons */
  cursor: pointer;
  /* Change cursor to pointer on hover */
  display: inline-block;
  /* Make sure buttons are side by side */
}

.icon-button img {
  width: 30px;
  height: 30px;
}

.icon-button:focus {
  outline: none;
  /* Remove focus outline */
}
</style>