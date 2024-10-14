import { get } from "https";
import {PeriodChecker, check60Days, check90Days, getDaysDifference, formatDate} from "../frontend/src/util/periodPolicy.js";

// Step 1: Do isolated unit tests on the helper functions -> getDaysDifference, formatDate
// Step 2: Do integration tests on the helper functions -> check60Days, check90Days
// Step 3: Test PeriodChecker with mock helper functions.??
// wah shag why I have so many helper functions


describe('formatDate unit testing', () =>{
    test('Check that date object is converted to YYYY-MM-DD as expected', () =>{
        const timestamp = new Date('2024-08-01T00:48:06+08:00');
        const result = formatDate(timestamp);
        expect(result).toBe('2024-08-01')
    })
});

describe('getDaysDifference unit testing', () =>{
    test('Check that the difference between two formatted date strings is correct', () =>{
        const date1 = '2024-10-15';
        const date2 = '2025-01-15';
        const result = getDaysDifference(date1, date2);
        expect(result).toBe(92);
    })
});

// check60Days implements getDaysDifference -> integration
describe('check60Days integration testing', () => {
    test('If start date is exactly 2 months from ago, start date is valid (boundary)', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2024-08-15"
        expect(check60Days(currentDate, checkDate)).toBe(true);
    })
    test('If start date is within 2 months ago from today, but before the boundary date', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2024-08-18"
        expect(check60Days(currentDate,checkDate)).toBe(true);
    })
    test('If start date is beyond 2 months ago', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2024-08-14"
        expect(check60Days(currentDate,checkDate)).toBe(false);
    })
});

// check90Days implements getDaysDifference -> integration
describe('check90Days integration testing', () => {
    test('If start date is exactly 3 months later, start date is valid (boundary)', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2025-01-15"
        expect(check90Days(currentDate, checkDate)).toBe(true);
    })
    test('If start date is within 3 months in the future, but before the boundary date', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2024-12-12"
        expect(check90Days(currentDate,checkDate)).toBe(true);
    })
    test('If start date is beyond 3 months later', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2025-01-16"
        expect(check90Days(currentDate,checkDate)).toBe(false);
    })
});

// check90Days implements getDaysDifference -> integration
describe('check90Days integration testing', () => {
    test('If start date is exactly 3 months later, start date is valid (boundary)', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2025-01-15"
        expect(check90Days(currentDate, checkDate)).toBe(true);
    })
    test('If start date is within 3 months in the future, but before the boundary date', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2024-12-12"
        expect(check90Days(currentDate,checkDate)).toBe(true);
    })
    test('If start date is beyond 3 months later', () =>{
        const currentDate = "2024-10-15"
        const checkDate = "2025-01-16"
        expect(check90Days(currentDate,checkDate)).toBe(false);
    })
});



