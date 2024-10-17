// convert timestamp to YYYY-MM-DD for period policy
export function formatDate(date) {
    const year = date.getFullYear(); // Get the full year
    const month = String(date.getMonth() + 1).padStart(2, '0'); // Get the month (0-based, hence +1) and pad with 0 if needed
    const day = String(date.getDate()).padStart(2, '0'); // Get the day and pad with 0 if needed

    return `${year}-${month}-${day}`; // Return the formatted date string
}

// find the difference between currentDate and checkDate
export function getDaysDifference(date1Str, date2Str) {
    // Convert the date strings to Date objects
    const date1 = new Date(date1Str);
    const date2 = new Date(date2Str);
    
    // Reset the time portion to midnight (00:00:00) for both dates
    date1.setHours(0, 0, 0, 0);
    date2.setHours(0, 0, 0, 0);

    // Get the difference in time (milliseconds)
    const timeDifference = Math.abs(date2 - date1);

    // Convert the time difference from milliseconds to days
    const dayDifference = timeDifference / (1000 * 60 * 60 * 24);

    return dayDifference;
}


// dates YYYY-MM-DD, use formatDate() to format your date objects first
export function check60Days(currentDate, checkDate){
    console.log("60 DAYS IS TRIGGERED")
    console.log(getDaysDifference(currentDate, checkDate))
    if(getDaysDifference(currentDate, checkDate) > 61){
        return false;
    }
    return true;
}

export function check90Days(currentDate, checkDate){
    console.log("90 DAYS IS TRIGGERED")
    console.log(getDaysDifference(checkDate, currentDate))
    if(getDaysDifference(checkDate, currentDate) > 92){
        return false;
    }
    return true;
}


export function PeriodChecker(checkDate){
    const currentDate = formatDate(new Date());
    if(checkDate < currentDate){
        console.log("60 DAYS: " + check60Days(currentDate, checkDate))
        return check60Days(currentDate, checkDate);
    }
    else{
        console.log("90 DAYS: " + check60Days(currentDate, checkDate))
        return check90Days(currentDate, checkDate);
    }
}