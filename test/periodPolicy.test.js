import * as periodPolicy from "../frontend/src/util/periodPolicy.js";
// import {PeriodChecker, check60Days, check90Days, getDaysDifference, formatDate} from "../frontend/src/util/periodPolicy.js";
// import {PeriodChecker, formatDate} from "../frontend/src/util/periodPolicy.js";



// describe('formatDate unit testing', () =>{
//     test('Check that date object is converted to YYYY-MM-DD as expected', () =>{
//         const timestamp = new Date('2024-08-01T00:48:06+08:00');
//         const result = formatDate(timestamp);
//         expect(result).toBe('2024-08-01')
//     })
// });

// describe('getDaysDifference unit testing', () =>{
//     test('Check that the difference between two formatted date strings is correct', () =>{
//         const date1 = '2024-10-15';
//         const date2 = '2025-01-15';
//         const result = getDaysDifference(date1, date2);
//         expect(result).toBe(92);
//     })
// });


// describe('check60Days testing', () => {
//     test('If start date is exactly 2 months from ago, start date is valid (boundary)', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2024-08-15"
//         expect(check60Days(currentDate, checkDate)).toBe(true);
//     })
//     test('If start date is within 2 months ago from today, but before the boundary date', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2024-08-18"
//         expect(check60Days(currentDate,checkDate)).toBe(true);
//     })
//     test('If start date is beyond 2 months ago', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2024-08-14"
//         expect(check60Days(currentDate,checkDate)).toBe(false);
//     })
// });


// describe('check90Days testing', () => {
//     test('If start date is exactly 3 months later, start date is valid (boundary)', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2025-01-15"
//         expect(check90Days(currentDate, checkDate)).toBe(true);
//     })
//     test('If start date is within 3 months in the future, but before the boundary date', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2024-12-12"
//         expect(check90Days(currentDate,checkDate)).toBe(true);
//     })
//     test('If start date is beyond 3 months later', () =>{
//         const currentDate = "2024-10-15"
//         const checkDate = "2025-01-16"
//         expect(check90Days(currentDate,checkDate)).toBe(false);
//     })
// });


jest.mock('../frontend/src/util/periodPolicy.js', () => ({
    ...jest.requireActual('../frontend/src/util/periodPolicy.js'), // Retain other exports
    check60Days: jest.fn(),
    check90Days: jest.fn(),
}));

describe('PeriodChecker testing', () => {
    beforeEach(() => {
        // Clear mock calls before each test
        periodPolicy.check60Days.mockClear();
        periodPolicy.check90Days.mockClear();
    });

    test('If checkDate is earlier than currentDate, invoke check60Days', () => {
        const currentDate = "2024-10-18";
        const checkDate = "2024-09-15";

        periodPolicy.PeriodChecker(currentDate, checkDate);

        // Expect check60Days to be called
        expect(periodPolicy.check60Days).toHaveBeenCalledWith(currentDate, checkDate);
        expect(periodPolicy.check90Days).not.toHaveBeenCalled(); // Ensure check90Days was not called
    });

    test('If checkDate is later than currentDate, invoke check90Days', () => {
        const currentDate = "2024-10-18";
        const checkDate = "2024-11-15";

        PeriodChecker(currentDate, checkDate);

        // Expect check90Days to be called
        expect(periodPolicy.check90Days).toHaveBeenCalledWith(currentDate, checkDate);
        expect(periodPolicy.check60Days).not.toHaveBeenCalled(); // Ensure check60Days was not called
    });

    test('If checkDate is the same as currentDate, invoke check90Days', () => {
        const currentDate = "2024-10-18";
        const checkDate = "2024-10-18";

        PeriodChecker(currentDate, checkDate);

        // Expect check90Days to be called
        expect(periodPolicy.check90Days).toHaveBeenCalledWith(currentDate, checkDate);
        expect(periodPolicy.check60Days).not.toHaveBeenCalled(); // Ensure check60Days was not called
    });
});



