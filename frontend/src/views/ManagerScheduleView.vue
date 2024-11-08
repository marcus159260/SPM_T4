<template>
  <div class="wrapper">
  <div class="manager-wrapper">
    <!-- Tabs navs -->
    <ul class="nav nav-tabs mb-3" id="ex1" role="tablist">
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link active" id="ex1-tab-1" href="#ex1-tabs-1" role="tab"
          aria-controls="ex1-tabs-1" aria-selected="true">Pending</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-2" href="#ex1-tabs-2" role="tab" aria-controls="ex1-tabs-2"
          aria-selected="false">Approved</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-3" href="#ex1-tabs-3" role="tab" aria-controls="ex1-tabs-3"
          aria-selected="false">Rejected</a>
      </li>
      <li class="nav-item" role="presentation">
        <a data-mdb-tab-init class="nav-link" id="ex1-tab-4" href="#ex1-tabs-4" role="tab" aria-controls="ex1-tabs-4"
          aria-selected="false">All Requests</a>
      </li>
    </ul>
    <!-- Tabs navs -->

    <!-- Tabs content -->
    <div class="tab-content" id="ex1-content">

      <!--Pending WFH-->
      <div class="tab-pane fade show active" id="ex1-tabs-1" role="tabpanel" aria-labelledby="ex1-tab-1">
        <ViewPendingRequests :managerId="managerId" :role="role"/>
      </div>
      <!--End of Pending WFH-->

      <!--Approved WFH-->
      <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
        <ApprovedRequests :managerId="managerId" :role="role"/>
      </div>
      <!--End of Approved WFH-->

      <!--Rejected WFH-->
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        <RejectedRequests :managerId="managerId" :role="role"/>
      </div>
      <!--End of Rejected WFH-->

      <!--All Requests-->
      <div class="tab-pane fade" id="ex1-tabs-4" role="tabpanel" aria-labelledby="ex1-tab-4">
        <AllRequests :managerId="managerId" :role="role"/>
      </div>
      <!--End of All Requests-->

    </div>
    <!-- Tabs content -->
  </div>
</div>

</template>

<script>
import { Tab, initMDB } from "mdb-ui-kit";
import { MDCRipple } from '@material/ripple';
import 'jquery';
import ViewPendingRequests from '../components/ManagerScheduleView/ViewPendingRequests.vue';
import AllRequests from '../components/ManagerScheduleView/AllRequests.vue';
import ApprovedRequests from '@/components/ManagerScheduleView/ApprovedRequests.vue';
import RejectedRequests from '@/components/ManagerScheduleView/RejectedRequests.vue';
import PopupWrapper from '@/components/PopupWrapper.vue';
import { useAuthStore } from '@/stores/auth';

export default {
  name: "ManagerView",
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
      managerId: null,
      role: null
    }
  },
  components: {
    ViewPendingRequests,
    AllRequests,
    ApprovedRequests,
    RejectedRequests,
    PopupWrapper
  },
  created() {
    this.managerId = this.authStore.user.staff_id || null;
    this.role = this.authStore.user.role || null;
    // console.log('Parent managerId:', this.managerId);
    // console.log(this.role);
  },
  computed: {
    authStore() {
      return useAuthStore();
    },
  }
}

</script>

<style>
.manager-wrapper {
  margin-top: 100px;
  margin-left: 100px;
  margin-right: 100px;
  margin-bottom: 200px;
}

@media(max-width: 400px) {
  .manager-wrapper {
    margin-top: 20px;
    margin-left: 20px;
    margin-right: 20px;
    margin-bottom: 20px;
  }
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

.wrapper {
  margin-top:-50px;
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