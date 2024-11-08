<template>
  <div id="main">
    <h6 id="pending-header" v-if="managerDetails" class="mt-10">
      Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
      Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
      Department: <span>{{ managerDetails.Department }}</span> <br />
      Position: <span>{{ managerDetails.Position }}</span> <br />
    </h6>

    <button @click="fetchRequests" class="btn btn-primary mt-3">Refresh Requests</button>
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
            <th scope="col" class="fixed-column">Approval</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="staff in filteredRequests" :key="staff.Staff_ID">
            <td data-cell="request id">{{ staff.Request_ID }}</td>
            <td data-cell="staff name">{{ staff.Staff_Name }}</td>
            <td data-cell="department">{{ staff.Staff_Department }}</td>
            <td data-cell="position">{{ staff.Staff_Position }}</td>
            <td data-cell="status" class="table-cell">
              <span :class="{
                'badge rounded-pill text-bg-success': staff.Status === 'Approved',
                'badge rounded-pill text-bg-warning': staff.Status === 'Pending' || staff.Status === 'Withdrawn - Pending',
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

            <!--Approve/Reject buttons-->
            <td data-cell="approval" class="fixed-column d-flex align-items-center">
              <button v-if="staff.Status == 'Withdrawn - Pending'" @click="approveWithdrawalRequest(staff.Request_ID)"
                class="icon-button mb-5" style="padding-top: 40px;">
                <img src="../../assets/checked.png" alt="Approve Withdrawal">
              </button>
              <button v-if="staff.Status == 'Pending'" @click="approveRequest(staff.Request_ID)"
                class="icon-button mb-5" style="padding-top: 40px;">
                <img src="../../assets/checked.png" alt="Approve">
              </button>


              <button @click="rejectRequestPopup(staff.Request_ID, staff.Status)" class="icon-button mb-5"
                style="padding-top: 40px;">
                <img src="../../assets/x-button.png" alt="Reject">
              </button>
            </td>
            <!--End of Approve/Reject buttons-->
          </tr>
        </tbody>
      </table>
      <div v-if="filteredRequests.length === 0" class="text-center mt-3">
                <p>No Pending Requests.</p>
      </div>
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
      filteredRequests: [],
      isPopupVisible: false,
      rejectionReason: '',
      withdrawalReason: '',
      selectedRequestStatus: '',
      selectedRequestId: null,
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
  components: {
    PopupWrapper
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
          const matchesStatus = request.Status === 'Pending' || request.Status === 'Withdrawn - Pending';

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
    approveRequest(requestId) {
      // console.log("Request ID clicked:", requestId); 
      axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/approve`, { managerId: this.managerId, Request_ID: requestId, request_Status: 'Approved' })
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
              axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/approve`, { managerId: this.managerId, Request_ID: requestId, request_Status: 'Approved', force_approval: true })  // Adding a flag for forced approval
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
      axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/approvewithdrawal`, { Request_ID: requestId, Manager_ID: this.managerId })
        .then(response => {
          // console.log('response.data', response.data);
          console.log('approveWithdrawalRequest');
          alert(response.data.message);
          this.fetchRequests();
        })
        .catch(error => {
          console.error('Error rejecting request:', error);
          alert(error.response.data.error);
        });
    },

    rejectRequestPopup(requestId, status) {
      this.selectedRequestId = requestId; // Store the request ID for rejection
      this.selectedRequestStatus = status;
      console.log(status);
      this.isPopupVisible = true; // Show the popup
      document.getElementById('popup').style.display = 'flex';
      // document.getElementById('popup').style.border = '1px black solid';
    },
    rejectRequest(requestId) {
      axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/reject`, { Request_ID: requestId, Rejection_Reason: this.rejectionReason, Manager_ID: this.managerId })
        .then(response => {
          console.log('response.data', response.data);
          alert(response.data.message);
          this.rejectionReason = '';
          this.fetchRequests();
          this.isPopupVisible = false; // Hide the popup after submission
          document.getElementById('popup').style.border = '';


        })
        .catch(error => {
          console.error('Error rejecting request:', error);
          if (error.response.data.error == 'Reason cannot be empty.') {
            // console.log(response.data.error);
            console.log('error from popup: no error msg');
            document.getElementById('errormsg').innerHTML = `Reason cannot be empty.<br>`;

          }
        });
    },
    rejectWithdrawalRequest(requestId) {
      axios.post(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/requests/rejectwithdrawal`, { Request_ID: requestId, Withdrawal_Reason: this.rejectionReason, Manager_ID: this.managerId })
        .then(response => {
          console.log('response.data', response.data);
          alert(response.data.message);
          this.fetchRequests();
          this.rejectionReason = '';
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
    // this.managerId = this.authStore.user.staff_id || null;
    // console.log(this.managerId);
    // console.log(this.role);
    this.fetchRequests();
    this.get_manager_details();
  },
};
</script>

<style scoped>
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

.date-column {
  min-width: 120px;
  /* Adjust width as needed */
}

.fixed-column {
  position: sticky;
  right: 0;
  z-index: 1;
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