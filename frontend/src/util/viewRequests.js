import { PeriodChecker } from "./periodPolicy";

export function viewRequests(currentDate, requests){
    const requestsArray = [];
    for(let request of requests){
       let valid = PeriodChecker(currentDate, request.Start_Date);
       if(valid){
        requestsArray.push(request);
       }
    }
    // console.log(requestsArray)
    return requestsArray;
}