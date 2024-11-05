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
          aria-selected="false">Rejected</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-5" href="#ex1-tabs-5" role="tab" aria-controls="ex1-tabs-5"
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
        <ViewPendingRequests 
        />

      </div>
      <!--End of Pending WFH-->

      <!--Approved WFH-->
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        <ApprovedRequests />
      </div>
      <!--End of Approved WFH-->

      <!--Rejected WFH-->
      <div class="tab-pane fade" id="ex1-tabs-4" role="tabpanel" aria-labelledby="ex1-tab-4">
        <RejectedRequests />
      </div>
      <!--End of Rejected WFH-->

      <!--All Requests-->
      <div class="tab-pane fade" id="ex1-tabs-5" role="tabpanel" aria-labelledby="ex1-tab-5">
        <AllRequests />
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
import ApprovedRequests from '@/components/ManagerScheduleView/ApprovedRequests.vue';
import RejectedRequests from '@/components/ManagerScheduleView/RejectedRequests.vue';
import PopupWrapper from '@/components/PopupWrapper.vue';

import { useAuthStore } from '../stores/auth';


export default {
  name: "ManagerView",
  mounted() {
    initMDB({ Tab }); // Initialize the MDB tabs when the component is mounted
    // Initialize Ripple
    const rippleSurface = Array.prototype.slice.call(document.querySelectorAll('.ripple-surface'))
    rippleSurface.map(s => {
      return new MDCRipple(s)
    })

    // this.managerId = this.authStore.user?.managerId || null;
    // this.get_employees_by_dept();
    console.log(this.authStore.user)
    this.managerId = this.authStore.user.staff_id || null;
    console.log(this.managerId)
  },
  data() {
    return {
      employees: [], //initialize
      managerId: null,
      isLoading: true // Add loading state
    }
  },
  computed: {
    authStore() {
      return useAuthStore(); // Access the auth store
    },
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
      axios.get(`http://127.0.0.1:5000/api/users/by-dept-employees`)
        .then(response => {
          this.employees = response.data.data; // Assign fetched data to the staffSchedules array
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
    ApprovedRequests,
    RejectedRequests,
    PopupWrapper
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

#popup {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  /* -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale; */
  /* text-align: center; */
  color: #2c3e50;
  background-color: white;
  /* border: 1px black solid; */
  border-radius: 5px;
  position: fixed;
  /* Fixes the popup to the viewport */
  z-index: 1;
  /* Ensures it appears above other content */
  left: 50%;
  /* Move to the middle of the screen */
  top: 50%;
  /* Move to the middle of the screen */
  transform: translate(-50%, -50%);
  /* Offset by half its width and height */
  /* background: #3794ff; */
  color: #fff;
  width: 500px;
  /* Set width */
  min-height: min-content;
  /* Set height */
  display: none;
  /* Enables flexbox for centering content */
  padding: 0px;
  /* align-items: center; Vertically center content */
  /* justify-content: center; Horizontally center content */
}


/* .popover {
  margin: 0;
  font-size: 14px;
  text-transform: uppercase;
  background: #fff;
  color: #3794ff;
  padding: 2px 2px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.popover:hover {
  background: #2b2b2b;
  color: #fff;
}

.popover-content {
  position: absolute;
  background: #fff;
  border-radius: 1px;
  margin-top: 4px;
  padding: 2px;
  color: #333;
  min-width: 200px;
  text-align: left;
} */
</style>