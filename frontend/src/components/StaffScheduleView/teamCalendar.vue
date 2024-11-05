<template>
    <CalendarNavigation
    :currentDate="config.startDate"
    :earliestDate="earliestDate"
    :latestDate="latestDate"
    @dateChanged="onDateChanged"
  />
  <DayPilotScheduler :config="config" ref="schedulerRef" />
</template>

<script setup>
import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
import { ref, reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import CalendarNavigation from '../CalendarNavigation.vue';


import axios from 'axios';

const emit = defineEmits(['dateChanged']);


const config = reactive({
  timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
  scale: "CellDuration",
  cellDuration: 720,
  cellWidthSpec: "Auto",
  cellNumber: 2,
  days: 7,
  startDate: DayPilot.Date.today().firstDayOfWeek(),
  timeRangeSelectedHandling: "Disabled",
  Staff_ID: useAuthStore().user.staff_id,
  reporting_manager: 0,
  eventClickHandling: "Disabled",
  eventHoverHandling: "Bubble",
  bubble: new DayPilot.Bubble({
    onLoad: function(args) {
    var ev = args.source;
    console.log(ev.data);
    args.async = true;  // notify manually using .loaded()
    
    // simulating slow server-side load
    setTimeout(function() {
        args.html = "Request Details<br>" + ev.data.bubbleHtml;
        args.loaded();
    }, 500);
}
  }),
  treeEnabled: true,
});
const schedulerRef = ref(null);
  
  const today = DayPilot.Date.today();
  const currentDayOfWeek = today.getDayOfWeek(); // 1 = Monday, 7 = Sunday
  const daysToMonday = currentDayOfWeek - 1; // Subtract to get back to Monday
  const startOfWeek = today.addDays(-daysToMonday);

  config.startDate = startOfWeek;

  const earliestDate = startOfWeek.addDays(-60); // 60 days back
  const latestDate = startOfWeek.addDays(90);    // 90 days forward
  const changeView = () => {
      if (this.config.days === 7) {
        this.config.days = 1;
        this.config.startDate = DayPilot.Date.today();
      } else {
        this.config.days = 7;
        this.config.startDate = DayPilot.Date.today().firstDayOfWeek();
      }
      // Emit the event when the view changes
      this.$emit('view-changed');
    }
const find_manager_details= () => { 
    let url = `http://127.0.0.1:5000/api/users/find-manager/` + config.Staff_ID;
    axios.get(url)
      .then(response => {
        config.reporting_manager = response.data.data.Reporting_Manager; // Store manager details
        console.log(config.reporting_manager);

        loadResources();

      })
      .catch(error => {
        console.error("Error fetching manager details:", error);
      });
  };
  
  

const loadResources = () => {
  
  var teamurl = `http://127.0.0.1:5000/api/users/by-team-employees/` + config.reporting_manager;
  axios
    .get(teamurl)
    .then((response) => {
      console.log(response);
      var temp = response.data;
      var tempresources = [];
      for(let emp of temp.data){
        let resource = {id: "E_"+emp.id, name: emp.name,dept:emp.Dept,position:emp.Position};
        tempresources.push(resource);
      }

      config.resources = tempresources;
      console.log("Loaded resources:", config.resources);

      axios
        .get(`http://127.0.0.1:5000/api/wfh/all_events`, {
        headers: {
          'X-Staff-ID': useAuthStore().user.staff_id,
          'X-Staff-Role': useAuthStore().user.role,
        },
      })
        .then((r) => {
          
          if (r.data){
              console.log(r.data);
              for(let e of r.data){
                if(e.status == 'Approved'){

                  let bubbleHtml = `<ul><li>Date: `+new Date(e.start).toISOString().slice(0, 10)+ `</li><li>Time: `+e.time+`</li><li>Status: `+e.status+`</li><li>Request Type: `+ e.request_type+`</li></ul>`;
                  e.bubbleHtml = bubbleHtml;
                  config.events.push(e);

                }
                

              }
          }
        })
          .catch((error) => {
            console.error('Error fetching requests:', error);
          });

        
    }
  )
    .catch((error) => {
      console.error('Error fetching requests:', error);
    });
  
  console.log(config.resources);
  console.log(config.events);


};
function onDateChanged(newStartDate) {
  config.startDate = newStartDate;
  emit('dateChanged', newStartDate);
}
  
onMounted(() => {
  config.events = [];
  find_manager_details();
  
  // loadEvents();
  console.log(config.events);
  console.log(config.resources);
  console.log(config.Staff_ID);
});
</script>
