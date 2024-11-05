import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_cancel_request_success(client):
    request = {
        "Request_ID": 279,
        "Withdrawal_Reason": "test cancel",
        "Staff_id": 150076
    }
    response = client.post('/api/wfh/requests/cancel', json=request)
    assert response.status_code == 200
    
def test_cancel_request_fail(client):
    request = {
        "Withdrawal_Reason": "test cancel"
    }
    response = client.post('/api/wfh/requests/cancel', json=request)
    assert response.status_code == 400
    