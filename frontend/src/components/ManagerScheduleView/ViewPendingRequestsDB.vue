<template>
  <div>
    <h6 id="pending-header" v-if="filteredEmployee" class="mt-10">
      Manager Name: <span>{{ filteredEmployee.Manager_Name }}</span> <br />
      Manager ID: <span>{{ filteredEmployee.Reporting_Manager }}</span> <br>
      In charge of: <br>
      &emsp;Dept -> <span>{{ filteredEmployee.Dept }}</span> <br>
      &emsp;Position -> <span>{{ filteredEmployee.Position }}</span>
    </h6>

    <table class="table align-middle mt-10 bg-white" v-if="hasPendingRequests">
      <thead class="bg-light">
        <tr>
          <th>Staff_ID</th>
          <th>Name</th>
          <th>Department & Position</th>
          <th>Country</th>
          <th>Pending WFH Approval</th>
        </tr>
      </thead>

      <tbody>

        <tr v-for="staff in filteredPendingEmployees" :key="staff.Staff_ID">
          <td>
            <p class="mb-1">{{ staff.Staff_ID }}</p>
          </td>
          <td>
            <div class="d-flex align-items-center">
              <div class="ms-3">
                <p class="fw-bold mb-1">{{ staff.Staff_FName }} {{ staff.Staff_LName }}</p>
                <p class="text-muted mb-0">{{ staff.Email }}</p>
              </div>
            </div>
          </td>
          <td>
            <div class="d-flex align-items-center">
              <div class="ms-3">
                <p class="fw-bold mb-1">{{ staff.Dept }}</p>
                <p class="text-muted mb-0">{{ staff.Position }}</p>
              </div>
            </div>
          </td>
          <td>
            <p class="fw-normal mb-1">{{ staff.Country }}</p>
          </td>
          <td>
            <a href="#" class="d-inline-block">
              <img style="width:30px; height:30px" src="../../assets/checked.png">
            </a>
            <a href="#" class="d-inline-block ms-2">
              <img style="width:30px; height:30px" src="../../assets/x-button.png">
            </a>
          </td>
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
      selectedStatus: '',  // Holds the value selected in the dropdown
      allRequests: [],     // All WFH requests fetched from the API
      filteredRequests: [],  // The filtered WFH requests
    };
  },
  methods: {
    applyFilter() {
      // Filter the WFH requests based on the selected status
      if (this.selectedStatus === '') {
        // If no status is selected (i.e., "All"), show all requests
        this.filteredRequests = this.allRequests;
      } else {
        // Filter requests by the selected status
        this.filteredRequests = this.allRequests.filter(
          request => request.Status && request.Status.toLowerCase() === this.selectedStatus.toLowerCase()
        );
      }
    },
    fetchRequests() {
      // Fetch WFH requests using Axios
      axios.get('http://127.0.0.1:5000/api/wfh/requests')
        .then(response => {
          this.allRequests = response.data;
          this.filteredRequests = response.data;  // Initially show all requests
          console.log(response.data)
        })
        .catch(error => {
          console.error('Error fetching requests:', error);
        });
    },
  },
  mounted() {
    // Fetch requests when the component is mounted
    this.fetchRequests();
    console.log(this.filteredRequests)
  },
};
  </script>
  
<style scoped>

#pending-header span {
  color: green;
}
</style>