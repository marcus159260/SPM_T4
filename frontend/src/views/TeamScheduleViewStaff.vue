<!-- <template>
    <div>
      <teamCalendar
        :title="'My Team Schedule'"
        :resources="resources"
        @dateChanged="onDateChanged"

      />
    </div>
  </template>
  
  <script>
  import teamCalendar from '../components/StaffScheduleView/teamCalendar.vue';
  import { useAuthStore } from '@/stores/auth';
  
  export default {
    components: {
      teamCalendar,
    },
    data() {
      return {
        teamEvents: [],
        teamResources: [],
        employees:[],
        resources:[],
        Staff_ID: useAuthStore().user.staff_id

        
      };
    }
    
  };
  
  
  </script> -->

  <!-- ############################################################################################################################################################################ -->
  <template>
    <div>
      <CalendarNavigation
        :currentDate="startDate"
        :earliestDate="earliestDate"
        :latestDate="latestDate"
        @dateChanged="onDateChanged"
      />
      <teamManagerCalendar
        :resources="resources"
        :events="events"
        :startDate="startDate"
        :days="days"
      />
    </div>
  </template>
  <script>
  import teamManagerCalendar from '../components/teamCalendarManager.vue';
  import axios from 'axios';
  import { useAuthStore } from '@/stores/auth';
  import { DayPilot } from 'daypilot-pro-vue';
  import CalendarNavigation from '../components/CalendarNavigation.vue';
  
  export default {
    components: {
      teamManagerCalendar,
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
        reporting_manager: '',
      };
    },
  
    mounted() {
      this.find_manager_details();
    },
  
    methods: {
      find_manager_details(){ 
        let url = `http://127.0.0.1:5000/api/users/find-manager/` + this.authStore.user.staff_id;
        axios.get(url)
          .then(response => {
            this.reporting_manager = response.data.data.Reporting_Manager; // Store manager details
            console.log(this.reporting_manager);

            this.loadResources();

          })
          .catch(error => {
            console.error("Error fetching manager details:", error);
          });
      },
      loadResources() {
        var teamurl = `http://127.0.0.1:5000/api/users/by-team-employees/` + this.reporting_manager;
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
        this.loadEvents(); 
        }
        
      )
        .catch((error) => {
          console.error('Error fetching requests:', error);
        });
      },
  
      loadEvents() {
        axios
            .get(`http://127.0.0.1:5000/api/wfh/all_events`)
            .then((r) => {
              if (r.data){
                  console.log('all_events',r.data);
                  for(let e of r.data){
                      let bubbleHtml = `<ul><li>Date: `+new Date(e.start).toISOString().slice(0, 10)+`</li><li>Status: `+e.status+`</li></ul>`;
                    // console.log(bubbleHtml);
                      e.bubbleHtml = bubbleHtml;
                      e.text = 'WFH';
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
        // this.loadre();
        // this.loadEvents();
      },
    }
  
  };
  </script>
