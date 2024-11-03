import { PeriodChecker } from "./periodchecker/periodCheck";
import * as checkDays from "./periodchecker/checkDays";

const spy60 = jest.spyOn(checkDays, "check60Days").mockImplementation(() => {});
const spy90 = jest.spyOn(checkDays, "check90Days").mockImplementation(() => {});

describe ("please work", () =>{
    beforeEach(() => {
        jest.clearAllMocks();
    });

   test("If the start date is earlier than current date, invoke check60Days", () => {
    // const spy60 = jest.spyOn(checkDays, "check60Days").mockImplementation(() => {});
    const currentDate = "2024-10-18"
    const checkDate = "2024-09-18"
    PeriodChecker(currentDate, checkDate)
    expect(spy60).toHaveBeenCalledWith(currentDate, checkDate);
    expect(spy90).toHaveBeenCalledTimes(0);
   })

   test("If the start date is later than current date, invoke check90Days", () => {
    // const spy90 = jest.spyOn(checkDays, "check90Days").mockImplementation(() => {});
    const currentDate = "2024-10-18"
    const checkDate = "2024-11-18"
    PeriodChecker(currentDate, checkDate)
    expect(spy90).toHaveBeenCalledWith(currentDate, checkDate);
    expect(spy60).toHaveBeenCalledTimes(0);
   })

   test("If the start date is equal to current date, return true do not invoke the helper functions", () => {
    // const spy90 = jest.spyOn(checkDays, "check90Days").mockImplementation(() => {});
    const currentDate = "2024-10-18"
    const checkDate = "2024-11-18"
    PeriodChecker(currentDate, checkDate)
    expect(spy60).toHaveBeenCalledTimes(0);
    expect(spy60).toHaveBeenCalledTimes(0);
   })


})