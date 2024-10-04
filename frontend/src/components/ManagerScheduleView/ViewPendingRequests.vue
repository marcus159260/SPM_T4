<template>
  <div>
    <table v-if="pendingRequests.length > 0" class="table align-middle mt-10 bg-white">
      <thead class="bg-light">
        <tr>
          <th>Request_ID</th>
          <th>Name (Staff ID) & Position</th>
          <th>Request_Type / Time of WFH requested days</th>
          <th>Application_Date</th>
          <th>WFH_Start_Date</th>
          <th>WFH_End_Date</th>
          <th>Reason of Application</th>
          <th>Status</th>
          <th>Approver</th>
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
                <p class="fw-bold mb-1">{{ staff.Staff_Name }} ({{ staff.Staff_ID }})</p>
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
          <td>
            <p class="mb-1">{{ staff.Approver }}</p>
          </td>
          <!-- <td>
            <a href="#" class="d-inline-block">
              <img style="width:30px; height:30px" src="../../assets/checked.png">
            </a>
            <a href="#" class="d-inline-block ms-2">
              <img style="width:30px; height:30px" src="../../assets/x-button.png">
            </a>
          </td> -->
        </tr>

      </tbody>
    </table>

    <div v-else class="text-center mt-3">
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
    };
  },
  computed: {
    pendingRequests() {
      // Filter by status 'Pending' and order by Request_ID in ascending order
      return this.allRequests
        .filter(request => {
          const applicationDate = new Date(request.Application_Date); // Use Application_Date for filtering

          // Calculate the date 3 months from the Application_Date
          const threeMonthsFromApplicationDate = new Date(applicationDate);
          threeMonthsFromApplicationDate.setMonth(threeMonthsFromApplicationDate.getMonth() + 3);
          // console.log(applicationDate, "\n", threeMonthsFromApplicationDate)

          // Return true if the request is pending and the current date is within 3 months of the application date
          return request.Status === 'Pending' && new Date() <= threeMonthsFromApplicationDate;
        })
        .sort((a, b) => a.Request_ID - b.Request_ID); // Sort by Request_ID in ascending order
    },
  },
  methods: {
    fetchRequests() {
      // Fetch WFH requests using Axios
      axios.get('http://localhost:5000/api/wfh/requests')
        .then(response => {
          this.allRequests = response.data;
          // console.log(response.data)
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
  },
  mounted() {
    // Fetch requests when the component is mounted
    this.fetchRequests();
    console.log(this.allRequests)
  },
};
</script>

<style scoped>
/* Add your styles here */
</style>