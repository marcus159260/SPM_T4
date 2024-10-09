<template>
    <div>
        <h5 class="mt-4">Approved Requests</h5>
        <table v-if="approvedRequests.length > 0" class="table align-middle mt-10 bg-white">
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
                </tr>
            </thead>

            <tbody v-for="staff in approvedRequests" :key="staff.Staff_ID">
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
                </tr>
            </tbody>
        </table>

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
    computed: {
        computed: {
            pendingRequests() {
                return this.allRequests
                    .filter(request => {
                        const applicationDate = new Date(request.Application_Date);
                        const threeMonthsFromApplicationDate = new Date(applicationDate);
                        threeMonthsFromApplicationDate.setMonth(threeMonthsFromApplicationDate.getMonth() + 3);

                        return (
                            request.Status === 'Pending' &&
                            request.Approver_ID === this.managerId &&
                            new Date() <= threeMonthsFromApplicationDate
                        );
                    })
                    .sort((a, b) => a.Request_ID - b.Request_ID);
            },

            approvedRequests() {
                return this.allRequests
                    .filter(request => request.Status === 'Approved')
                    .sort((a, b) => a.Request_ID - b.Request_ID); // Sort by Request_ID
            },
        },

    }
};
</script>

<style scoped>
/* Add your styles here */
</style>