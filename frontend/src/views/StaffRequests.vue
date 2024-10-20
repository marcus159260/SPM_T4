<template>
  <div class="manager-wrapper">
    <!-- Tabs navs -->
    <ul class="nav nav-tabs mb-3" id="ex1" role="tablist">
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link active" id="ex1-tab-1" href="#ex1-tabs-1" role="tab"
          aria-controls="ex1-tabs-1" aria-selected="true">View My Schedule</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-2" href="#ex1-tabs-2" role="tab" aria-controls="ex1-tabs-2"
          aria-selected="false">View My Team Schedule</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-3" href="#ex1-tabs-3" role="tab" aria-controls="ex1-tabs-3"
          aria-selected="false">Create Request</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-4" href="#ex1-tabs-4" role="tab" aria-controls="ex1-tabs-4"
          aria-selected="false">Pending</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-5" href="#ex1-tabs-5" role="tab" aria-controls="ex1-tabs-5"
          aria-selected="false">Approved</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-6" href="#ex1-tabs-6" role="tab" aria-controls="ex1-tabs-6"
          aria-selected="false">All Requests</a>
      </li>
    </ul>
    <!-- Tabs navs -->

    <!-- Tabs content -->
    <div class="tab-content" id="ex1-content">

      <!--View My Schedule-->
      <div class="tab-pane fade show active" id="ex1-tabs-1" role="tabpanel" aria-labelledby="ex1-tab-1">
        <h1>Insert Staff View Own Schedule here</h1>
      </div>
      <!-- End of View My Schedule-->

      <!--View My Team Schedule-->
      <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
        <h1>Insert Staff View My Team Schedule here</h1>
      </div>
      <!--End of All Requests-->

      <!--Create Request-->
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        <ApplicationForm />
      </div>
      <!--End of All Requests-->

      <!--Pending WFH-->
      <div class="tab-pane fade" id="ex1-tabs-4" role="tabpanel" aria-labelledby="ex1-tab-4">
        <ViewPendingRequests />
      </div>

      <!--End of Pending WFH-->

      <!--Approved Requests-->
      <div class="tab-pane fade" id="ex1-tabs-5" role="tabpanel" aria-labelledby="ex1-tab-5">
        <ViewApprovedRequests />
      </div>
      <!--End of Approved Requests-->

      <!--All Requests-->
      <div class="tab-pane fade" id="ex1-tabs-6" role="tabpanel" aria-labelledby="ex1-tab-6">
        <ViewAllRequests2 />
      </div>
      <!--End of All Requests-->

    </div>
    <!-- Tabs content -->
  </div>
</template>

<script>
import { Tab, initMDB } from "mdb-ui-kit";
import { MDCRipple } from '@material/ripple';
import 'jquery';

import ViewPendingRequests from '../components/StaffScheduleView/ViewPendingRequests.vue';
import ViewApprovedRequests from '../components/StaffScheduleView/ViewApprovedRequests.vue';
import ViewAllRequests2 from '../components/StaffScheduleView/ViewAllRequests.vue';
import ApplicationForm from '../components/StaffScheduleView/ApplicationForm.vue';


export default {
  name: "StaffView",
  mounted() {
    initMDB({ Tab }); // Initialize the MDB tabs when the component is mounted
    // Initialize Ripple
    const rippleSurface = Array.prototype.slice.call(document.querySelectorAll('.ripple-surface'))
    rippleSurface.map(s => {
      return new MDCRipple(s)
    })
  },

  data() {
    return {
      employees: [], //initialize
      managerId: 151408,
      isLoading: true // Add loading state
    }
  },
  components: {
    ViewPendingRequests,
    ViewApprovedRequests,
    ViewAllRequests2,
    ApplicationForm
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
