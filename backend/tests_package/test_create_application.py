import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from freezegun import freeze_time

from routes.requests import create_request

# Integration test
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
    
    
