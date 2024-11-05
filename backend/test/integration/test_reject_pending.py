import pytest
import json
from app import app 
from util.db import supabase

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
def test_reject_pending_request_success(client):
    request = {
        "Request_ID": 247,
        "Rejection_Reason": 'test reject',
        "Staff_ID": 150076,
        "Manager_ID": 151408
        
    }
    response = client.post('/api/wfh/requests/reject', json=request)
    assert response.status_code == 200
    
def test_reject_pending_request_fail(client):
    request = {
        "Request_ID": 247,
        "Rejection_Reason": '',
        "Staff_ID": 150076,
        "Manager_ID": 151408
    }
    response = client.post('/api/wfh/requests/reject', json=request)
    print(response)
    assert response.status_code == 404