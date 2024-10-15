<template>
    <div class="request-form">
      <h2>Apply for a New Request</h2>
      <form @submit.prevent="submitRequest">
        <label for="requestType">Request Type:</label>
        <select v-model="requestType" id="requestType" required>
          <option value="ADHOC">ADHOC</option>
          <option value="RECURRING">RECURRING</option>
        </select>
  
        <label for="startDate">Start Date:</label>
        <input v-model="startDate" type="date" id="startDate" required />
  
        <label for="endDate" v-if="requestType === 'RECURRING'">End Date:</label>
        <input v-model="endDate" type="date" id="endDate" v-if="requestType === 'RECURRING'" required />
  
        <label for="time_of_day">Time:</label>
        <select v-model="timeOfDay" id="time_of_day" required>
          <option value="">Select Time</option>
          <option value="AM">AM</option>
          <option value="PM">PM</option>
          <option value="FULL">Full Day</option>
        </select>
  
        <label for="reason">Reason:</label>
        <textarea v-model="reason" id="reason" required></textarea>
  
        <button type="submit">Submit Request</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        staffId: 150076,
        requestType: "ADHOC",
        startDate: "",
        endDate: "",
        timeOfDay: "",  
        reason: "",
        approverId: 151408,
      };
    },
    methods: {
        
      // Submit the request data
      async submitRequest() {
        try {
            const formattedEndDate = this.endDate ? `${this.endDate}` : `${this.startDate}`;
            const payload = {
                staff_id: this.staffId,
                start_date: this.startDate, 
                end_date: formattedEndDate,    
                time_of_day: this.timeOfDay,   
                request_type: this.requestType,
                status: 'Pending',   
                reason: this.reason,
                approver_id: this.approverId,
                requested_dates: this.requestType === "ADHOC" ? [`${this.startDate}`] : this.generateRecurringDates()
            };

            const response = await axios.post('http://127.0.0.1:5000/api/wfh/requests', payload);
            console.log("Request submitted:", response.data);
        } catch (error) {
            console.error("Error submitting request:", error);
        }
    },
  
      generateRecurringDates() {
        const dates = [];
        let current = new Date(this.startDate);
  
        while (current <= new Date(this.endDate)) {
          dates.push(current.toISOString().split('T')[0]);  
          current.setDate(current.getDate() + 7); 
        }
  
        return dates;
      },
    },
  };
  </script>
  
  <style>
  .request-form {
    max-width: 500px;
    margin: 0 auto;
  }
  </style>
