<template>
  <div>
    <CalendarNavigation
      :currentDate="startDate"
      :earliestDate="earliestDate"
      :latestDate="latestDate"
      @dateChanged="onDateChanged"
    />
    <teamCalendar
      :resources="resources"
      :events="events"
      :startDate="startDate"
      :days="days"
    />
  </div>
</template>
<script>
import teamCalendar from '../components/teamCalendar.vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';
import { DayPilot } from 'daypilot-pro-vue';
import CalendarNavigation from '../components/CalendarNavigation.vue';

export default {
  components: {
    teamCalendar,
    CalendarNavigation
  },

  computed: {
    authStore() {
      return useAuthStore();
    },
  },
  data() {
    const today = DayPilot.Date.today();
    const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
    const daysToMonday = currentDayOfWeek - 1;
    const startOfWeek = today.firstDayOfWeek().addDays(1);
    return {
      resources: [],
      events: [],
      startDate: DayPilot.Date.today(),
      days: 7,
      earliestDate: startOfWeek.addDays(-60),
      latestDate: startOfWeek.addDays(90),
    };
  },

  mounted() {
    this.loadResources();
    this.loadEvents();
  },

  methods: {
    loadResources() {
      var teamurl = `${import.meta.env.VITE_API_BASE_URL}/api/users/by-team-employees/` + this.authStore.user.staff_id;
    // console.log(teamurl);
    axios
      .get(teamurl)
      .then((response) => {
        // console.log(response);
        console.log(response);
      var temp = response.data;
      var tempresources = [];
      for(let emp of temp.data){
        let resource = {id: "E_"+emp.id, name: emp.name+"\n"+emp.Dept+" ("+emp.Position+")",dept:emp.Dept,position:emp.Position};
        tempresources.push(resource);
      }
      this.resources = tempresources;
      console.log("Loaded resources:", this.resources);  
      }
    )
      .catch((error) => {
        console.error('Error fetching requests:', error);
      });
    },

    loadEvents() {
      axios
          .get(`${import.meta.env.VITE_API_BASE_URL}/api/wfh/all_events`)
          .then((r) => {
            if (r.data){
                console.log('all_events',r.data);
                for(let e of r.data){
                    let bubbleHtml = `<ul><li>Date: `+new Date(e.start).toISOString().slice(0, 10)+`</li><li>Status: `+e.status+`</li></ul>`;
                    e.bubbleHtml = bubbleHtml;
                    e.text = 'WFH'
                    this.events.push(e);
                }
            }
          })
            .catch((error) => {
              console.error('Error fetching requests:', error);
            });
    },

    onDateChanged(newStartDate) {
      this.startDate = newStartDate;
      this.loadResources();
    },
  }

};
</script>