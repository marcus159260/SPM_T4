export const check60Days = (currentDate, checkDate) => {
    console.log("60 days triggered, " + currentDate + " - " + checkDate)
    if(getDaysDifference(currentDate, checkDate) > 61){
        return false;
    }
    return true;
}

export const check90Days = (currentDate, checkDate) => {
    console.log("90 days triggered, " + currentDate + " - " + checkDate)
    if(getDaysDifference(checkDate, currentDate) > 92){
        return false;
    }
    return true;
}