import pytest
import json
from app import app 
from unittest.mock import MagicMock
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Integration test with check_conflict and supabase
def test_submit_application_with_no_conflict(client):
    request = {
        "approver_id": 151408,
        "end_date": "2024-12-26",
        "reason": "after christmas party",
        "request_type": "ADHOC",
        "requested_dates": ['2024-12-26'],
        "staff_id": 150076,
        "start_date": "2024-12-26",
        "status": "Pending",
        "time_of_day": "PM"
    }
    response = client.post('/api/wfh/requests', json=request)
    assert response.status_code == 201
    
# Integration test with check_conflict and supabase
def test_submit_application_with_conflict(client):
    request = {
        "approver_id": 151408,
        "end_date": "2024-12-26",
        "reason": "after christmas party",
        "request_type": "ADHOC",
        "requested_dates": ['2024-12-26'],
        "staff_id": 150076,
        "start_date": "2024-12-26",
        "status": "Pending",
        "time_of_day": "PM"
    }
    response = client.post('/api/wfh/requests', json=request)
    assert response.status_code == 400
    
    # Delete the test request so can run the test repeatedly with no conflict.
    supabase.table('request').delete().eq('Staff_ID', 150076).eq('Start_Date', '2024-12-26').execute()
    
    
    
    

