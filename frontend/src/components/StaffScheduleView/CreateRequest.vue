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
        timeOfDay: "",  // Holds the value from dropdown
        reason: "",
        approverId: 151408,  // Approver ID, can be fetched dynamically
      };
    },
    methods: {
        
      // Submit the request data
      async submitRequest() {
        try {
            const formattedEndDate = this.endDate ? `${this.endDate}` : `${this.startDate}`;
            const payload = {
                staff_id: this.staffId,
                start_date: this.startDate, // Ensure it's formatted as 'YYYY-MM-DD'
                end_date: formattedEndDate,     // Ensure it's formatted as 'YYYY-MM-DD'
                time_of_day: this.timeOfDay,    // AM/PM/FULL from dropdown
                request_type: this.requestType,
                status: 'Pending',          // Default status
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
  
      // For RECURRING requests, generate dates (assuming recurring Mondays logic)
      generateRecurringDates() {
        const dates = [];
        let current = new Date(this.startDate);
  
        while (current <= new Date(this.endDate)) {
          dates.push(current.toISOString().split('T')[0]);  // Get YYYY-MM-DD format
          current.setDate(current.getDate() + 7);  // Move to next Monday
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
