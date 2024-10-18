import { check60Days, check90Days} from "./checkDays"


export const PeriodChecker = (currentDate, checkDate) =>{

    if(checkDate < currentDate){
        const result = check60Days(currentDate, checkDate);
        return result;
    }
    else if(checkDate > currentDate){
        const result = check90Days(currentDate, checkDate);
        return result
    }
    else{
        return true
    }
}