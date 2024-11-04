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
    cellWidthSpec: "Auto",
    cellNumber: 2,
    days: 7,
    startDate: DayPilot.Date.today().firstDayOfWeek(),
    timeRangeSelectedHandling: "Disabled",
    Staff_ID: 150076,
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
    
    
  
  // const loadEvents = () => {
  //   loadResources();
  //   const events = [
  //     { id: 1, start: "2024-10-01", end: "2024-10-05", text: "WFH", resource: "R" },
  //     { id: 2, start: DayPilot.Date.today(), end: DayPilot.Date.today().addDays(5), text: "WFO", resource: "R2" }
  //   ];

  //   var resources = config.resources;
  //   console.log(resources);

  //   for(emp of resources){
  //     var requesturl = "http://127.0.0.1:5000/api/wfh/" + emp.id;

  //     axios
  //       .get(requesturl)
  //       .then((response) => {
  //         data = response.data;
  //         temp = [];
  //         for(e of data){
  //           let bubbleHtml = `<ul><li>Start Date: `+e.Start_Date+`</li><li>End Date: `+ e.End_Date+ `</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+`</li></ul>`;
  //           console.log(bubbleHtml);
  //           config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
  //         }
          
  //         console.log("Loaded resources:", this.resources);
  //       })
  //       .catch((error) => {
  //         console.error('Error fetching requests:', error);
  //       });

  //   }
    
  //   // config.events = events;
  // };
  
  // const loadResources = () => {
    
  //   var teamurl = "http://127.0.0.1:5000/api/users/by-team-employees/" + config.reporting_manager;
  //   // console.log(teamurl);
  //   axios
  //     .get(teamurl)
  //     .then((response) => {
  //       // console.log(response);
  //       var temp = response.data;
  //       config.resources = temp.data;
  //       console.log("Loaded resources:", temp);
        
  //       for(let emp of temp.data){
  //         var requesturl = "http://127.0.0.1:5000/api/wfh/" + emp.id;

  //         axios
  //           .get(requesturl)
  //           .then((response) => {
  //             var data = response.data;
              
  //             if (data.data){
  //               // console.log(data.data);
  //               for(let e of data.data){
  //                 if(e.Status == 'Approved'){
  //                   let bubbleHtml = `<ul><li>Date: `+e.Start_Date+ `</li><li>Time: `+e.Time+`</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+`</li><li>Department: `+emp.Dept+`</li><li>Position: `+emp.Position+`</li></ul>`;
  //                 // console.log(bubbleHtml);
  //                 if(e.Time == 'AM'){
  //                   e.Start_Date += 'T00:00:00';
  //                   e.End_Date += 'T12:00:00';
  //                   console.log(e.Start_Date);
  //                 }
  //                 else if(e.Time == 'PM'){
  //                   e.Start_Date += 'T12:00:00';
  //                   e.End_Date += 'T24:00:00';
  //                 }
  //                 else if(e.Time =='FULL'){
  //                   e.Start_Date += 'T00:00:00';
  //                   e.End_Date += 'T24:00:00';
  //                 }
  //                 config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
                
  //                 }
  //                 }

  //             }
              

          
  //           })
  //           .catch((error) => {
  //             console.error('Error fetching requests:', error);
  //           });

  //       }
  //     })
  //     .catch((error) => {
  //       console.error('Error fetching requests:', error);
  //     });
    

  // };

  const loadResources = () => {
    
    var teamurl = "http://127.0.0.1:5000/api/users/by-team-employees/" + config.reporting_manager;
    // console.log(teamurl);
    axios
      .get(teamurl)
      .then((response) => {
        // console.log(response);
        var temp = response.data;
        config.resources = temp.data;
        console.log("Loaded resources:", temp);

        axios
          .get("http://127.0.0.1:5000/api/wfh/all_events")
          .then((r) => {
            
            if (r.data){
                console.log(r.data);
                for(let e of r.data){
                  if(e.status == 'Approved'){

                    let bubbleHtml = `<ul><li>Date: `+new Date(e.start).toISOString().slice(0, 10)+ `</li><li>Time: `+e.time+`</li><li>Status: `+e.status+`</li><li>Request Type: `+ e.request_type+`</li></ul>`;
                  // console.log(bubbleHtml);
                    e.bubbleHtml = bubbleHtml;
                    config.events.push(e);

                  }
                  

                }
            }
          })
            .catch((error) => {
              console.error('Error fetching requests:', error);
            });


        
        
        // for(let emp of temp.data){
        //   console.log(emp);
          
        //   let hasDigits = emp.id.split('').some(char => !isNaN(char) && char !== ' ');

        //   // Initialize cleanStaffId
        //   let cleanStaffId = '';

        //   if (hasDigits) {
        //       // Filter out only the digits and join them into a string
        //       cleanStaffId = staffId.split('').filter(char => !isNaN(char) && char !== ' ').join('');

        //       var requesturl = "http://127.0.0.1:5000/api/events/" + cleanStaffId;

        //   axios
        //     .get(requesturl)
        //     .then((response) => {
        //       var data = response.data;
              
        //       if (data.data){
        //         console.log(data.data);
        //         for(let e of data.data){
        //           if(e.Status == 'Approved'){
        //             let bubbleHtml = `<ul><li>Date: `+e.start+ `</li><li>Time: `+e.time+`</li><li>Status: `+e.Status+`</li><li>Request Type: `+ e.Request_Type+`</li><li>Department: `+emp.Dept+`</li><li>Position: `+emp.Position+`</li></ul>`;
        //           // console.log(bubbleHtml);
        //           if(e.Time == 'AM'){
        //             e.Start_Date += 'T00:00:00';
        //             e.End_Date += 'T12:00:00';
        //             console.log(e.Start_Date);
        //           }
        //           else if(e.Time == 'PM'){
        //             e.Start_Date += 'T12:00:00';
        //             e.End_Date += 'T24:00:00';
        //           }
        //           else if(e.Time =='FULL'){
        //             e.Start_Date += 'T00:00:00';
        //             e.End_Date += 'T24:00:00';
        //           }
        //           config.events.push({resource:e.Staff_ID,id:e.Request_ID,start: e.Start_Date, end:e.End_Date, time:e.Time, status:e.Status, text:"WFH", bubbleHtml:bubbleHtml});
                
        //           }
        //           }

        //       }
              

        //       // console.log("Loaded resources:", config.events);
              
          
        //     })
        //     .catch((error) => {
        //       console.error('Error fetching requests:', error);
        //     });

        // }
        //   }
          
      }
    )
      .catch((error) => {
        console.error('Error fetching requests:', error);
      });
    
    console.log(config.resources);
    console.log(config.events);


  };
  
  onMounted(() => {
    config.events = [];
    find_manager_details();
    
    // loadEvents();
    console.log(config.events);
    console.log(config.resources);
    console.log(config.Staff_ID);
  });
  </script>
  