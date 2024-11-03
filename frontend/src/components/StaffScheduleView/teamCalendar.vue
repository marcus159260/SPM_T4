<template>
    <DayPilotScheduler :config="config" ref="schedulerRef" />
  </template>
  
  <script setup>
  import { DayPilot, DayPilotScheduler } from 'daypilot-pro-vue';
  import { ref, reactive, onMounted } from 'vue';
  import axios from 'axios';
  
  const config = reactive({
    timeHeaders: [{"groupBy":"Month"},{"groupBy":"Day","format":"d"},{"groupBy":"Cell","format":"tt"}],
    scale: "CellDuration",
    cellDuration: 720,
    days: DayPilot.Date.today().daysInMonth(),
    startDate: DayPilot.Date.today().firstDayOfMonth(),
    timeRangeSelectedHandling: "Disabled",
    reporting_manager: 140894,
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
  
  const loadEvents = () => {
    loadResources();
    const events = [
      { id: 1, start: "2024-10-01", end: "2024-10-05", text: "WFH", resource: "R" },
      { id: 2, start: DayPilot.Date.today(), end: DayPilot.Date.today().addDays(5), text: "WFO", resource: "R2" }
    ];

    var resources = config.resources;
    console.log(resources);

    for(emp of resources){
      var requesturl = "http://127.0.0.1:5000/api/wfh/" + emp.id;

      axios
        .get(requesturl)
        .then((response) => {
          data = response.data;
          temp = [];
          for(e of data){
            let bubbleHtml = `<ul><li>Start Date: `+e.Start_Date+`</li><li>End Date: `+ e.End_Date+ `</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+`</li></ul>`;
            console.log(bubbleHtml);
            config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
          }
          
          console.log("Loaded resources:", this.resources);
        })
        .catch((error) => {
          console.error('Error fetching requests:', error);
        });

    }
    
    // config.events = events;
  };
  
  const loadResources = () => {
    // const resources = [
    //     {
    //         "name": "Alice",
    //         "test":123,
    //         "id": "R"
    //     },
    //     {
    //         "name": "Rachel",
    //         "id": "R2"
    //     }
    // ];
    var teamurl = "http://127.0.0.1:5000/api/users/by-team-employees/" + config.reporting_manager;
    // console.log(teamurl);
    axios
      .get(teamurl)
      .then((response) => {
        // console.log(response);
        var temp = response.data;
        config.resources = temp.data;
        console.log("Loaded resources:", temp);
        
        for(let emp of temp.data){
          var requesturl = "http://127.0.0.1:5000/api/wfh/" + emp.id;

          axios
            .get(requesturl)
            .then((response) => {
              var data = response.data;
              
              if (data.data){
                // console.log(data.data);
                for(let e of data.data){
                  let bubbleHtml = `<ul><li>Start Date: `+e.Start_Date+`</li><li>End Date: `+ e.End_Date+ `</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+`</li><li>Department: `+emp.Dept+`</li><li>Position: `+emp.Position+`</li></ul>`;
                  console.log(bubbleHtml);
                  config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
                }

              }
              

              // console.log("Loaded resources:", config.events);
              
          
            })
            .catch((error) => {
              console.error('Error fetching requests:', error);
            });

        }
      })
      .catch((error) => {
        console.error('Error fetching requests:', error);
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
  </script>
  