<template>
  <div class="manager-wrapper">
    <!-- Tabs navs -->
    <ul class="nav nav-tabs mb-3" id="ex1" role="tablist">
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link active" id="ex1-tab-1" href="#ex1-tabs-1" role="tab"
          aria-controls="ex1-tabs-1" aria-selected="true">View Staff Schedules</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-2" href="#ex1-tabs-2" role="tab" aria-controls="ex1-tabs-2"
          aria-selected="false">Pending</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-3" href="#ex1-tabs-3" role="tab" aria-controls="ex1-tabs-3"
          aria-selected="false">Approved</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-4" href="#ex1-tabs-4" role="tab" aria-controls="ex1-tabs-4"
          aria-selected="false">All Requests</a>
      </li>
    </ul>
    <!-- Tabs navs -->

    <!-- Tabs content -->
    <div class="tab-content" id="ex1-content">

      <!--View Staff Schedules-->
      <div class="tab-pane fade show active" id="ex1-tabs-1" role="tabpanel" aria-labelledby="ex1-tab-1">

        <!--List filter, Calendar filter-->
        <div id="filter-view" class="d-flex justify-content-end">
          <button type="button" class="btn btn-outline-success m-1 w-auto">
            List View
            <span class="ripple-surface"></span>
          </button>

          <button type="button" class="btn btn-outline-primary m-1 w-auto calendar-btn">
            Calendar View
            <span class="ripple-surface"></span>
          </button>
        </div>
        <!--End of List filter, Calendar filter-->

        <table class="table align-middle mt-10 bg-white">
          <thead class="bg-light">
            <tr>
              <th>Staff_ID</th>
              <th>Name & Email</th>
              <th>Department & Position</th>
              <th>Country</th>
              <th>View Schedule</th>
              <th>Reporting Manager ID</th>
              <th>Reporting Manager Name</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="staff in employees" :key="staff.Staff_ID">
              <td>
                <p class="fw-normal mb-1">{{ staff.Staff_ID }}</p>
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
                <button type="button" class="btn btn-success rounded-pill px-4" data-bs-toggle="modal"
                  data-bs-target="#myModal">
                  View Schedule
                </button>
              </td>
              <td>
                <p class="fw-normal mb-1">{{ staff.Reporting_Manager }}</p>
              </td>
              <td>
                <p class="fw-normal mb-1">{{ staff.Manager_Name }}</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <!-- End of View Staff Schedules-->

      <!--Pending WFH-->
      <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
        <!-- <ViewPendingRequestsDB
          v-if="employees.length > 0" 
          :filteredEmployee="filteredEmployee" 
          :filteredPendingEmployees="filteredPendingEmployees" 
          :hasPendingRequests="hasPendingRequests" 
        /> -->
        <ViewPendingRequests/>
      </div>
      <!--End of Pending WFH-->
      

      <!--Approved WFH-->
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        <!-- <ViewPendingRequestsDB
          v-if="employees.length > 0" 
          :filteredEmployee="filteredEmployee" 
          :filteredPendingEmployees="filteredPendingEmployees" 
          :hasPendingRequests="hasPendingRequests" 
        /> -->
        <ApprovedRequests/>
      </div>
      <!--End of Approved WFH-->


      <!--All Requests-->
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        <AllRequests />
      <div class="tab-pane fade" id="ex1-tabs-4" role="tabpanel" aria-labelledby="ex1-tab-4">
        <FilterRequests />
      </div>
      <!--End of All Requests-->

    </div>
    <!-- Tabs content -->
  </div>

</template>

<script>
import axios from 'axios';
import { Tab, initMDB } from "mdb-ui-kit";
import { MDCRipple } from '@material/ripple';
import 'jquery';
// import ViewPendingRequestsDB from '../components/ManagerScheduleView/ViewPendingRequestsDB.vue';
import ViewPendingRequests from '../components/ManagerScheduleView/ViewPendingRequests.vue';

import AllRequests from '../components/ManagerScheduleView/AllRequests.vue';
import FilterRequests from '../components/ManagerScheduleView/FilterRequests.vue';

export default {
  name: "ManagerView",
  mounted() {
    initMDB({ Tab }); // Initialize the MDB tabs when the component is mounted
    // Initialize Ripple
    const rippleSurface = Array.prototype.slice.call(document.querySelectorAll('.ripple-surface'))
    rippleSurface.map(s => {
      return new MDCRipple(s)
    })

    // Fetch data from the Flask back-end
    // this.get_employees_callCentre(); //call methods
    this.get_employees_by_dept();
  },

  data() {
    return {
      employees: [], //initialize
      managerId: 140001,
      isLoading: true // Add loading state
    }
  },
  computed: {
    filteredEmployee() {
      // Filter employees based on Dept and Position
      return (
        this.employees.find(
          (staff) =>
            staff.Dept === "Engineering" &&
            staff.Position === "Call Centre" &&
            staff.Reporting_Manager === this.managerId
        ) || {}
      );
    },

    filteredPendingEmployees() {
      // Filter employees based on manager ID, department, and position
      return (this.employees.filter(
        (staff) =>
          // staff.Dept === "Engineering" &&
          // staff.Position === "Call Centre" &&
          staff.Reporting_Manager === this.managerId
        ) || []
      );
    },

    hasPendingRequests() {
      return this.filteredPendingEmployees.length > 0; // Returns true if there are pending requests
    },
  },
  methods: {
    get_employees_by_dept() {
      axios.get('http://localhost:5000/api/users/by-dept-employees')
        .then(response => {
          this.employees = response.data.data; // Assign fetched data to the staffSchedules array
          console.log(this.employees)
          this.isLoading = false;
        })
        .catch(error => {
          console.error("Error fetching schedules:", error);
          this.isLoading = false;
        });
      
        
    }
  },
  components: {
    // ViewPendingRequestsDB,
    ViewPendingRequests,
    AllRequests,
    FilterRequests
    
  },
}


</script>

<style>
.manager-wrapper {
  margin-top: 100px;
  margin-left: 100px;
  margin-right: 100px;
  margin-bottom: 200px;
}

</style>