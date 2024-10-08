<template>
    <div>
      <h6>Approved Requests</h6>
      <table v-if="approvedRequests.length > 0" class="table align-middle mt-10 bg-white">
        <thead class="bg-light">
          <tr>
            <th>Request_ID</th>
            <th>Name & Staff_ID</th>
            <th>Department & Position</th>
            <th>Application_Date</th>
            <th>Start_Date</th>
            <th>End_Date</th>
            <th>Reason</th>
          </tr>
        </thead>
        <tbody v-for="request in approvedRequests" :key="request.Request_ID">
          <tr>
            <td>{{ request.Request_ID }}</td>
            <td>{{ request.Staff_Name }} ({{ request.Staff_ID }})</td>
            <td>{{ request.Staff_Department }} - {{ request.Staff_Position }}</td>
            <td>{{ request.Application_Date }}</td>
            <td>{{ request.Start_Date }}</td>
            <td>{{ request.End_Date }}</td>
            <td>{{ request.Reason }}</td>
          </tr>
        </tbody>
      </table>
      <div v-else class="text-center mt-3">
        <p>No approved requests.</p>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      approvedRequests: {
        type: Array,
        default: () => [],
      },
    },
  };
  </script>
  
  <style scoped>
  /* Add your styles here */
  </style>
  