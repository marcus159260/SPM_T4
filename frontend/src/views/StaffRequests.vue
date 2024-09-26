<template>
    <div>
        <h6 class="mt-5">Name: {{ staff_fname }} {{staff_lname}}</h6>
        <table class="table">
        <thead>
            <tr>
            <th scope="col">Request ID</th>
            <th scope="col">Request Type</th>
            <th scope="col">Status</th>
            <th scope="col">Start Date</th>
            <th scope="col">End Date</th>
            <th scope="col">Reason</th>
            <th scope="col">Application Date</th>
            <th scope="col">Approver</th>
            </tr>
        </thead>
        <tbody>
            <tr v-for="request in requestsData" :key="request.request_id">
                <th scope="row">{{ request.request_id }}</th>
                <td>{{ request.request_type}}</td>
                <td>{{ request.status}}</td>
                <td>{{ formatDate(request.start_date) }}</td>
                <td>{{ formatDate(request.end_date) }}</td>
                <td>{{ request.reason }}</td>
                <td>{{ formatDate(request.application_date) }}</td>
                <td>{{ request.approver }}</td>
            </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
export default {
    name: "StaffRequests",
    data(){
        return{
            staff_fname: "Oliver",
            staff_lname: "Chan",
            requestsData : [
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