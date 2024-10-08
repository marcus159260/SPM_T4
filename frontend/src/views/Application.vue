<template>
    <div>
        <h1>werk from home application</h1>
        <div class = " d-flex justify-content-center">
            <div class="card w-75 align-items-center">
                <div class="card-body">
                    <h3>Application form you've been waiting for...</h3>
                    <form @submit.prevent>
                        <!-- ATC1 : If selected adhoc & start date, autopopulate end date = start date -->
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault1" checked>
                            <label class="form-check-label" for="flexRadioDefault1">
                                Adhoc
                            </label>
                            </div>
                            <div class="form-check">
                            <input class="form-check-input" type="radio" name="flexRadioDefault" id="flexRadioDefault2">
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
                        <!-- ATC4 (application): Start date must be earlier or equal to end date -->
                        <span class="text-danger" v-if="startEndDate == false">Your end date can't be earlier than start date</span>

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
            approver_id: 151408, //need to do some mounted function where we fetch staff_id + reporting mgr
            startDate: null,
            endDate: null,
            wfhTime: 'AM',
            requestReason: null,
            validPeriod: null
        }
    },
    methods:{
        checkPeriod(){
            this.validPeriod = PeriodChecker(this.startDate);
        }
    },
    computed:{
        canSubmit(){
            if(this.requestReason && this.checkPeriod && this.startEndDate){
                return true;
            } return false;
        },
        startEndDate(){
            if(this.startDate <= this.endDate){
                return true
            } return false;
        }
    }
    
}


</script>