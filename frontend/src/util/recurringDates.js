export function generateRecurringDates(startDate, endDate) {
    const dates = [];
    let current = new Date(startDate);

    while (current <= new Date(endDate)) {
      dates.push(current.toISOString().split('T')[0]);  // Get YYYY-MM-DD format
      current.setDate(current.getDate() + 7);  // Move to next Monday
    }

    return dates;
  }