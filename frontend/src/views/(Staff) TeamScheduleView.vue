<template>
    <div>
      <teamCalendar
        :title="'My Team Schedule'"
        :resources="resources"
      />
    </div>
  </template>
  
  <script>
  import teamCalendar from '../components/StaffScheduleView/teamCalendar.vue';
  import axios from 'axios';
  import { ref, reactive, onMounted } from 'vue';
  // import { getTeamEvents, getTeamResources } from '../services/apiService';
  
  const loadResources = () => {
      
      var teamurl = `http://127.0.0.1:5000/api/users/by-team-employees/` + config.reporting_manager;
      // console.log(teamurl);
      axios
        .get(teamurl)
        .then((response) => {
          // console.log(response);
          var temp = response.data;
          config.resources = temp.data;
          console.log("Loaded resources:", temp);
          
          for(let emp of temp.data){
            var requesturl = `http://127.0.0.1:5000/api/wfh/` + emp.id;
  
            axios
              .get(requesturl)
              .then((response) => {
                var data = response.data;
                
                if (data.data){
                  // console.log(data.data);
                  for(let e of data.data){
                    let bubbleHtml = `<ul><li>Start Date: `+e.Start_Date+`</li><li>End Date: `+ e.End_Date+ `</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+'</li><li>'+ emp.Dept+`</li><li>`+emp.Position+`</li></ul>`;
                    console.log(bubbleHtml);
                    config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
                  }
  
                }
                
            
              })
              .catch((error) => {
                console.error('Error fetching requests:', error);
              });
  
          }
  
          
        })
        .catch((error) => {
          console.error('Error fetching users:', error);
        });
      
      // console.log(config.resources);
  
  
    };
    
    onMounted(() => {
      config.events = [];
      loadResources();
      // loadEvents();
      console.log(config.events);
      console.log(config.resources);
    
      
    });
  
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
        Reporting_Manager: 140894 //hardcode team manager
        
      };
    },
    // mounted() {
    // //   var url = `http://127.0.0.1:5000/api/users/by-team-employees/` + this.Reporting_Manager;
    // //   axios
    // //     .get(url)
    // //     .then((response) => {
    // //       this.resources = response.data;
    // //       console.log("Loaded resources:", this.resources);
    // //     })
    // //     .catch((error) => {
    // //       console.error('Error fetching requests:', error);
    // //     });
    // // },
    
    // }
    };
  
  
  </script>