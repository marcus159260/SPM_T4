<template>
    <div >
        <div class = "d-flex justify-content-center">
            <div class="card w-75 h-100 align-items-center">
                <div class="card-body w-75">
                    <h4>{{ staff_name }}</h4>
                   
                    <form @submit.prevent>

                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" value="ADHOC" v-model="requestType" checked>
                            <label class="form-check-label" for="flexRadioDefault1">
                                Adhoc
                            </label>
                        </div>

                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2" value="RECURRING" v-model="requestType">
                            <label class="form-check-label" for="flexRadioDefault2">
                                Recurring
                            </label>
                        </div>

                        <div class="mb-3">
                            <label for="startDate" class="form-label">Start Date</label>
                            <input type="date" class="form-control" id="StartDate" v-model="startDate" @input = "checkPeriod">
                            <span class="text-danger" v-if="validPeriod == false">Start date can only be 2 months back or 3 months forward</span>
                        </div>

                        <div class="mb-3" v-if="requestType === 'RECURRING'">
                            <label for="endDate" class="form-label">End Date</label>
                            <input type="date" class="form-control" id="endDate" v-model="endDate" @input = "checkDateRange">
                            <span class="text-danger" v-if="validRecurringDuration == false">The start and end dates for a recurring request cannot be more than 3 months apart. Please try again.</span>
                        </div>
                        <!-- ATC4 (application): Start date must be earlier or equal to end date (recurring) -->
                        <span class="text-danger" v-if="startEndDate == false && endDate != null">Your end date can't be earlier than start date</span>

                        <div class="mb-3">
                            <label for="wfhTime" class="form-label">WFH time</label>
                            <select class="form-select" aria-label="wfhTime" v-model="wfhTime">
                                <option selected value="AM"> AM (9am - 1pm)</option>
                                <option value="PM">PM (2pm - 6pm)</option>
                                <option value="FULL">FULL (9am - 6pm)</option>
                            </select>
                        </div>

                        <div class="mb-3">
                            <label for="requestReason" class="form-label">Request Reason</label>
                            <input type="textarea" class="form-control" id="requestReason" v-model="requestReason">
                        </div>


                        <button type="submit" class="btn btn-primary" :disabled = "canSubmit == false" @click="submitRequest">Submit</button>
                    
                        
                </form>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import { formatDate, PeriodChecker, check90Days} from '@/util/periodPolicy';
import { generateRecurringDates } from '@/util/recurringDates';

export default{
    name: "ApplicationForm",
    data(){
        return{
            staffId: 150076, 
            staff_name: "",
            approverId: "", //need to do some mounted function where we fetch staff_id + reporting mgr
            startDate: null,
            endDate: null,
            wfhTime: 'AM',
            requestReason: null,
            requestType: "ADHOC",
            validPeriod: null,
            validRecurringDuration: null,
            isRequestReasonValid: true,
        }
    },
    methods:{
        async getStaffApprover(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/api/users/${this.staffId}`);
                if(response.data){
                    this.staff_name = response.data.data.Staff_FName + " " + response.data.data.Staff_LName;
                    this.approverId = response.data.data.Reporting_Manager;
                    
                }
                else{
                    console.log("No data found for this staff ID");
                }
            } catch(error){
                console.error("Error fetching staff details:", error);
            }
        },
        checkPeriod(){
            const currentDate = formatDate(new Date());
            this.validPeriod = PeriodChecker(currentDate, this.startDate);
        },
        checkDateRange() {
            const startDateCheck = new Date(this.startDate);
            const endDateCheck = new Date(this.endDate);
            this.validRecurringDuration = check90Days(startDateCheck, endDateCheck)
    },
        validateRequestReason() {
            this.isRequestReasonValid = this.requestReason.length > 0 ;
            console.log(this.isRequestReasonValid);
        },
        async submitRequest() {
            try {
                const formattedEndDate = this.endDate ? `${this.endDate}` : `${this.startDate}`;
                const payload = {
                    staff_id: this.staffId,
                    start_date: this.startDate,
                    end_date: formattedEndDate,  
                    time_of_day: this.wfhTime, 
                    request_type: this.requestType,
                    status: 'Pending', 
                    reason: this.requestReason,
                    approver_id: this.approverId,
                    requested_dates: this.requestType === "ADHOC" ? [`${this.startDate}`] : generateRecurringDates(this.startDate, this.endDate)
                };
                console.log(payload);

                const response = await axios.post('http://127.0.0.1:5000/api/wfh/requests', payload);
                if (response.data.message) {
                    console.log("Request submitted:", response.data);
                    alert('Request submitted successfully');
                }
                this.clearFields();
            }   catch (error) {
                    if (error.response && error.response.data.error) {
                    // conflict error message
                    alert(error.response.data.error); 
                } else {
                console.error("Error submitting request:", error);
            }
        }
    },
        clearFields(){
            this.staffId = null;
            this.startDate = null;
            this.endDate = null;
            this.wfhTime = null;
            this.requestType = "ADHOC";
            this.requestReason = null;
            this.validPeriod = null;
            this.validRecurringDuration = null;
        }

    },
    computed:{
        canSubmit(){
            if(this.requestReason && this.requestReason.length > 0 && this.validPeriod && this.startEndDate == true){
                return true;
            } return false;
        },
        startEndDate(){
            if(this.requestType == "RECURRING" && this.endDate !== null && this.startDate <= this.endDate){
                return true;
            }
            else if(this.requestType == "ADHOC" && this.startDate !== null){
                return true
            }
            return false;
        }
    },
    mounted(){
        this.getStaffApprover();
    }
    
}


</script>