import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from freezegun import freeze_time

from routes.requests import check_conflict

# Unit test on overlapping adhoc request
def test_overlapping_adhoc_requests():
    adhoc_request = {
        "approver_id": 151408,
        "end_date": "2024-10-22",
        "reason": "check overlap",
        "request_type": "ADHOC",
        "requested_dates": ['2024-10-22'],
        "staff_id": 150076,
        "start_date": "2024-10-22",
        "status": "Pending",
        "time_of_day": "PM"
    }
    response = check_conflict(adhoc_request["staff_id"], adhoc_request["requested_dates"], adhoc_request["time_of_day"])
    assert response != 'No conflict'
    
# Unit test on overlapping recurring request
def test_overlapping_recurring_requests():
    adhoc_request = {
        "approver_id": 151408,
        "end_date": "2024-10-22",
        "reason": "check overlap",
        "request_type": "ADHOC",
        "requested_dates": ['2024-12-04', '2024-12-11', '2024-12-18', '2024-12-25'],
        "staff_id": 150076,
        "start_date": "2024-10-22",
        "status": "Pending",
        "time_of_day": "PM"
    }
    response = check_conflict(adhoc_request["staff_id"], adhoc_request["requested_dates"], adhoc_request["time_of_day"])
    assert response != 'No conflict'
    
    
    
    
