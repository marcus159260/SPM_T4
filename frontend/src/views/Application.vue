<template>
    <div >
        <h1>werk from home application</h1>
        <div class = "d-flex justify-content-center">
            <div class="card w-75 h-100 align-items-center">
                <div class="card-body w-75">
                    <h1>{{ staff_name }}</h1>
                    <h3>{{endDate}}</h3>
                    <form @submit.prevent>

                        <!-- ATC1 : If selected adhoc & start date, autopopulate end date = start date -->
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
                            <input type="date" class="form-control" id="StartDate" aria-describedby="emailHelp" v-model="startDate" @input = "checkPeriod">
                            <span class="text-danger" v-if="validPeriod == false">Girl, it's 2 months back, 3 months forward for start date periodT</span>
                        </div>

                        <div class="mb-3">
                            <label for="endDate" class="form-label">End Date</label>
                            <input type="date" class="form-control" id="endDate" v-model="endDate">
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


                        <button type="submit" class="btn btn-primary" :disabled = "canSubmit == false">Submit</button>
                    
                        
                </form>
                </div>
            </div>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import { formatDate, PeriodChecker } from '@/util/periodPolicy';

export default{
    name: 'Application',
    data(){
        return{
            staff_id: 150076, //Oliver Chan werking it again!,
            staff_name: "",
            approver_name: "", //need to do some mounted function where we fetch staff_id + reporting mgr
            startDate: null,
            endDate: null,
            wfhTime: 'AM',
            requestReason: null,
            requestType: "ADHOC",
            validPeriod: null
        }
    },
    methods:{
        async getStaffApprover(){
            try{
                const response = await axios.get(`http://127.0.0.1:5000/api/users/${this.staff_id}`);
                if(response.data){
                    this.staff_name = response.data.data.Staff_FName + " " + response.data.data.Staff_LName;
                    this.approver_name = response.data.data.Reporting_Manager;
                }
                else{
                    console.log("No data found for this staff ID");
                }
            } catch(error){
                console.error("Error fetching requests:", error);
            }
        },
        checkPeriod(){
            this.validPeriod = PeriodChecker(this.startDate);
        },

    },
    computed:{
        canSubmit(){
            if(this.requestReason && this.requestReason.length > 10 && this.checkPeriod && this.startEndDate){
                return true;
            } return false;
        },
        startEndDate(){
            if(this.startDate <= this.endDate){
                return true
            } return false;
        }
    },
    mounted(){
        this.getStaffApprover();
    }
    
}


</script>