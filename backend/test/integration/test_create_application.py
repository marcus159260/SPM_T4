import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch, MagicMock

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
    
    
# Log activity is none
@patch('routes.requests.log_activity')
def test_submit_application_with_log_activity_none(mock_log_activity, client):
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
    log_mock_response = MagicMock()
    log_mock_response.data = None
    mock_log_activity.return_value = log_mock_response
    
    response = client.post('/api/wfh/requests', json=request)
    assert response.status_code == 201
    
    # Delete the test request so can run the test repeatedly with no conflict.
    supabase.table('request').delete().eq('Staff_ID', 150076).eq('Start_Date', '2024-12-26').execute()
    
    
supabase.table('request').delete().eq('Staff_ID', 150076).eq('Start_Date', '2024-12-26').execute()
    
  
@patch('util.db.supabase.rpc')  # Mocking the Supabase RPC
def test_create_request_401(mock_rpc, client):
    # Mock the RPC response to simulate failure in creating a request
    mock_response = MagicMock()
    # Here, we return a 'data' attribute as it would be returned in a real Supabase response
    mock_response.data = []  # Simulating no data returned from the RPC
    mock_response.execute.return_value = mock_response  # Mock the execute method to return this response
    mock_rpc.return_value = mock_response

    # Mock log_activity to avoid side effects in the test
    # mock_log_activity.return_value = MagicMock(data=None)

    # Prepare test data
    request_data = {
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

    # Send POST request to /api/wfh/requests with the mock data
    response = client.post('/api/wfh/requests', json=request_data)

    # Assert that the response status is 401 and the error message is as expected
    assert response.status_code == 401
    
@patch('util.db.supabase.rpc')  # Mocking the Supabase RPC
def test_create_request_500(mock_rpc, client):
    # Mock the RPC response to simulate failure in creating a request
    mock_response = MagicMock()
    mock_response.execute.return_value = {'data': []}  # Simulate no data returned from the RPC
    mock_rpc.return_value = mock_response

    # Mock log_activity to avoid side effects in the test
    # mock_log_activity.return_value = MagicMock(data=None)

    # Prepare test data
    request_data = {
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

    # Send POST request to /api/wfh/requests with the mock data
    response = client.post('/api/wfh/requests', json=request_data)

    # Assert that the response status is 401 and the error message is as expected
    assert response.status_code == 500
    
    

