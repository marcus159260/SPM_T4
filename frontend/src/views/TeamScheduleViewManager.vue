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
      var teamurl = `http://127.0.0.1:5000/api/users/all-staff-under-manager/` + this.authStore.user.staff_id;
    axios
      .get(teamurl)
      .then((response) => {
        console.log(response);
      var temp = response.data;
      this.resources = temp;
      
      axios
      .get(`http://127.0.0.1:5000/api/users/` + this.authStore.user.staff_id)
      .then((r) => {
        console.log(r);
        let manager = {};
        manager.id = "E_"+r.data.data['Staff_ID'];
        manager.name = r.data.data['Staff_FName'] + " " + r.data.data['Staff_LName'] +"\n"+ r.data.data.Dept+ " ("+ r.data.data['Position']+")";
        this.resources.unshift(manager);
      }
      )
      .catch((error) => {
          console.error('Error fetching manager details:', error);
        });

      console.log("Loaded resources:", this.resources);  
      }
    )
    },

    loadEvents() {
      axios
          .get(`http://127.0.0.1:5000/api/wfh/all_events`)
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
    },
  }

};
</script>