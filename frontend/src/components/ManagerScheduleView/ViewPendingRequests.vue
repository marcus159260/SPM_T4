<template>
  <div>
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
            <button @click="rejectRequest(staff.Request_ID)" class="icon-button mb-5" style="padding-top: 40px;">
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      allRequests: [],     // All WFH requests fetched from the API
      managerDetails: [],
      managerId: 151408,
    };
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
      axios.get(`http://localhost:5000/api/users/get-manager/${managerId}`)
        .then(response => {
          this.managerDetails = response.data.data; // Store manager details
          console.log(this.managerDetails)
        })
        .catch(error => {
          console.error("Error fetching manager details:", error);
        });
    },
    fetchRequests() {
      // Fetch WFH requests using Axios
      axios.get('http://localhost:5000/api/wfh/requests')
        .then(response => {
          this.allRequests = response.data;
          console.log(this.allRequests)
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
    approveRequest(requestId) {
      // console.log("Request ID clicked:", requestId); 
      axios.put(`http://localhost:5000/api/wfh/requests/${requestId}`, { Status: 'Approved' })
        .then(response => {
          const approvedRequest = this.allRequests.find(request => request.Request_ID === requestId);
          if (approvedRequest) {
            console.log(111)
            approvedRequest.Status = 'Approved';
            
          }
          this.fetchRequests();
        })
        .catch(error => {
          console.error('Error approving request:', error);
        });
    },

    rejectRequest(requestId) {
      // Try changing PATCH to PUT or POST depending on what the API expects
      axios.put(`http://localhost:5000/api/wfh/requests/${requestId}`, { Status: 'Rejected' }) // Changed to PUT
        .then(response => {
          const rejectedRequest = this.allRequests.find(request => request.Request_ID === requestId);
          if (rejectedRequest) {
            rejectedRequest.Status = 'Rejected';
          }
          this.fetchRequests();
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