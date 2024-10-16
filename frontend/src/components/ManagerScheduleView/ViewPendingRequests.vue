<template>
  <div id="main">
    <h6 id="pending-header" v-if="managerDetails" class="mt-10">
      Manager Name: <span>{{ managerDetails.Full_Name }}</span> <br />
      Manager ID: <span>{{ managerDetails.Staff_ID }}</span> <br>
      Department: <span>{{ managerDetails.Department }}</span> <br />
      Position: <span>{{ managerDetails.Position }}</span> <br />
      <!-- In charge of: <br>
          &emsp;Dept -> <span>{{ managerDetails.Department }}</span> <br>
          &emsp;Position -> <span>{{ managerDetails.Position }}</span> -->
    </h6>

    <table v-if="pendingRequests.length > 0" class="table align-middle mt-10 bg-white">
      <thead class="bg-light">
        <tr>
          <th>Request_ID</th>
          <th>Name & Staff_ID</th>
          <th>Department & Position</th>
          <th>Request_Type / Time of WFH requested days</th>
          <th>Application_Date</th>
          <th>WFH_Start_Date</th>
          <th>WFH_End_Date</th>
          <th>Reason of Application</th>
          <th>Status</th>
          <th>Approval</th>
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
            <p class="mb-1">{{ staff.End_Date }}</p>
          </td>
          <td>
            <p class="mb-1">{{ staff.Reason }}</p>
          </td>
          <td>
            <p class="mb-1">{{ staff.Status }}</p>
          </td>
          <!-- <td>
            <p class="mb-1">{{ staff.Approver }}</p>
          </td> -->

          <!--Approve/Reject buttons-->

          <!-- <td>
            <a href="#" class="d-inline-block">
              <img style="width:30px; height:30px" src="../../assets/checked.png">
            </a>
            <a href="#" class="d-inline-block ms-2">
              <img style="width:30px; height:30px" src="../../assets/x-button.png">
            </a>
          </td> -->


          <td class="d-flex align-items-center">
            <button @click="approveRequest(staff.Request_ID)" class="icon-button mb-5" style="padding-top: 40px;">
              <img src="../../assets/checked.png" alt="Approve">
            </button>
            <button @click="rejectRequestPopup(staff.Request_ID)" class="icon-button mb-5" style="padding-top: 40px;">
              <img src="../../assets/x-button.png" alt="Reject">
            </button>

          </td>


          <!--End of Approve/Reject buttons-->
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
                placeholder="Enter reason for rejection" />
              <div class="d-flex flex-column my-2">
                <p id="errormsg" class="text-danger mx-0"></p>
                <button type="button" class="btn btn-primary" @click="rejectRequest(selectedRequestId)">Submit</button>
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

export default {
  data() {
    return {
      allRequests: [],     // All WFH requests fetched from the API
      managerDetails: [],
      managerId: 151408,
      isPopupVisible: false,
      rejectionReason: ''
    };
  },
  components: {
    PopupWrapper
  },
  computed: {
    pendingRequests() {
      // Filter by status 'Pending' and Approver_ID matching managerId
      return this.allRequests
        .filter(request => {
          const applicationDate = new Date(request.Application_Date); // Use Application_Date for filtering

          // Calculate the date 3 months from the Application_Date
          const threeMonthsFromApplicationDate = new Date(applicationDate);
          threeMonthsFromApplicationDate.setMonth(threeMonthsFromApplicationDate.getMonth() + 3);

          // Return true if the request is pending, the current date is within 3 months of the application date, and the Approver_ID matches managerId
          return (
            request.Status === 'Pending' &&
            request.Approver_ID === this.managerId &&
            new Date() <= threeMonthsFromApplicationDate
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
      axios.get('http://127.0.0.1:5000/api/wfh/requests')
        .then(response => {
          console.log(123);
          this.allRequests = response.data;
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
    approveRequest(requestId) {
      // console.log("Request ID clicked:", requestId); 
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/approve`, { Request_ID: requestId, request_Status: 'Approved' })
        .then(response => {
          console.log('response.data', response.data);
          if (response.data == 'error') {
            alert("Cannot approve request as less than 50% of the team will be in the office")
          }
          else {
            this.fetchRequests();
          }
        })
        .catch(error => {
          console.error('Error rejecting request:', error);
        });
    },

    rejectRequestPopup(requestId) {
      this.selectedRequestId = requestId; // Store the request ID for rejection
      this.isPopupVisible = true; // Show the popup
      document.getElementById('popup').style.display = 'flex';
      document.getElementById('popup').style.border = '1px black solid';
    },
    rejectRequest(requestId) {
      axios.post(`http://127.0.0.1:5000/api/wfh/requests/reject`, { Request_ID: requestId, Rejection_Reason: this.rejectionReason })
        .then(response => {
          console.log('response.data', response.data);
          if (response.data == 'error') {
            // console.log(response.data.error);
            console.log('error from popup: no error msg');
            document.getElementById('errormsg').innerHTML = `Reason cannot be empty<br>`;

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

  },
  mounted() {
    // Fetch requests when the component is mounted
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
