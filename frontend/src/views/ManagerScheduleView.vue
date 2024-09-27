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
    </ul>
    <!-- Tabs navs -->

    <!-- Tabs content -->
    <div class="tab-content" id="ex1-content">

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

        <table class="table align-middle mb-0 bg-white">
          <thead class="bg-light">
            <tr>
              <th>Name</th>
              <th>Title</th>
              <th>Status</th>
              <th>Position</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>
                <div class="d-flex align-items-center">
                  <img src="https://mdbootstrap.com/img/new/avatars/8.jpg" alt="" style="width: 45px; height: 45px"
                    class="rounded-circle" />
                  <div class="ms-3">
                    <p class="fw-bold mb-1">John Doe</p>
                    <p class="text-muted mb-0">john.doe@gmail.com</p>
                  </div>
                </div>
              </td>
              <td>
                <p class="fw-normal mb-1">Software engineer</p>
                <p class="text-muted mb-0">IT department</p>
              </td>
              <td>
                <span class="text-black badge badge-success rounded-pill d-inline">Active</span>
              </td>
              <td>Senior</td>
              <td>
                <button type="button" class="btn btn-link btn-sm btn-rounded">
                  Edit
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex align-items-center">
                  <img src="https://mdbootstrap.com/img/new/avatars/6.jpg" class="rounded-circle" alt=""
                    style="width: 45px; height: 45px" />
                  <div class="ms-3">
                    <p class="fw-bold mb-1">Alex Ray</p>
                    <p class="text-muted mb-0">alex.ray@gmail.com</p>
                  </div>
                </div>
              </td>
              <td>
                <p class="fw-normal mb-1">Consultant</p>
                <p class="text-muted mb-0">Finance</p>
              </td>
              <td>
                <span class="text-black badge badge-primary rounded-pill d-inline">Onboarding</span>
              </td>
              <td>Junior</td>
              <td>
                <button type="button" class="btn btn-link btn-rounded btn-sm fw-bold" data-mdb-ripple-color="dark">
                  Edit
                </button>
              </td>
            </tr>
            <tr>
              <td>
                <div class="d-flex align-items-center">
                  <img src="https://mdbootstrap.com/img/new/avatars/7.jpg" class="rounded-circle" alt=""
                    style="width: 45px; height: 45px" />
                  <div class="ms-3">
                    <p class="fw-bold mb-1">Kate Hunington</p>
                    <p class="text-muted mb-0">kate.hunington@gmail.com</p>
                  </div>
                </div>
              </td>
              <td>
                <p class="fw-normal mb-1">Designer</p>
                <p class="text-muted mb-0">UI/UX</p>
              </td>
              <td>
                <span class="text-black badge badge-warning rounded-pill d-inline">Awaiting</span>
              </td>
              <td>Senior</td>
              <td>
                <button type="button" class="btn btn-link btn-rounded btn-sm fw-bold" data-mdb-ripple-color="dark">
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div class="tab-pane fade" id="ex1-tabs-2" role="tabpanel" aria-labelledby="ex1-tab-2">
        No pending requests.
      </div>
      <div class="tab-pane fade" id="ex1-tabs-3" role="tabpanel" aria-labelledby="ex1-tab-3">
        No approved requests.
      </div>
    </div>
    <!-- Tabs content -->
  </div>
</template>

<script>
import { Tab, initMDB } from "mdb-ui-kit";
import { MDCRipple } from '@material/ripple';

export default {
  name: "ManagerView",
  data() {
    return {
      staff_fname: "Oliver",
      staff_lname: "Chan",
      requestsData: [
        {
          request_id: 1,
          staff_id: 150076,
          staff_fname: 'Oliver',
          staff_lname: 'Chan',
          status: "Accepted",
          time: "AM",
          request_type: "Adhoc",
          start_date: "2024-09-25",
          end_date: "2024-09-25",
          reason: "Accompanying my mother to the clinic",
          application_date: "2024-09-25T10:30:00",
          approver: "Beata"
        },
        {
          request_id: 2,
          staff_id: 150076,
          staff_fname: 'Oliver',
          staff_lname: 'Chan',
          status: "Pending",
          time: "AM",
          request_type: "Adhoc",
          start_date: "2024-09-26",
          end_date: "2024-09-26",
          reason: "Lazy",
          application_date: "2024-09-25T10:30:00",
          approver: "Beata"
        },
        {
          request_id: 3,
          staff_id: 150076,
          staff_fname: 'Oliver',
          staff_lname: 'Chan',
          status: "Rejected",
          time: "AM",
          request_type: "Adhoc",
          start_date: "2024-10-01",
          end_date: "2024-10-01",
          reason: "Leave me alone, I wanna WFH",
          application_date: "2024-09-25T10:30:00",
          approver: "Beata"
        }
      ]
    }
  },
  mounted() {
    initMDB({ Tab }); // Initialize the MDB tabs when the component is mounted
    // Initialize Ripple
    const rippleSurface = Array.prototype.slice.call(document.querySelectorAll('.ripple-surface'))
    console.log(rippleSurface)
    rippleSurface.map(s => {
      return new MDCRipple(s)
    })

  },
  methods: {
    formatDate(dateString) {
      const date = new Date(dateString);
      const day = String(date.getDate()).padStart(2, '0');
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Months are zero-based
      const year = date.getFullYear();
      return `${day}-${month}-${year}`; // Format to DD-MM-YYYY
    }
  }
}
</script>

<style>
.manager-wrapper {
  margin-top: 100px;
  margin-left: 100px;
  margin-right: 100px;
}
</style>