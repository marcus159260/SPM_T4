import pytest
import json
from app import app 
from util.db import supabase

# TEST SCENARIO
# Login as Oliver Chan (ID = 150076)
# Withdraw specified request

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_withdraw_request_success(client):
    request = {
        "Request_ID": 224,
        "Rejection_Reason": "rejection test",
        "Staff_ID": 150076
    }
    response = client.post('/api/wfh/requests/withdraw', json=request)
    print(response)
    assert response.status_code == 200
    
    
def test_withdraw_request_fail(client):
    request = {
        "Request_ID": 163,
        "Rejection_Reason": "rejection test",
        "Staff_ID": 150076
    }
    response = client.post('/api/wfh/requests/withdraw', json=request)
    print(response)
    assert response.status_code == 400
    
# def test_withdraw_request_invalid_parameters():
    