import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_reject_withdrawal_no_request_found_fail(client):
    request = {
        "Request_ID": 124834394,
        "Withdrawal_Reason": "test withdraw"
    }
    response = client.post("/api/wfh/requests/rejectwithdrawal", json=request)
    assert response.status_code == 500
    
def test_reject_withdrawal_no_reason_fail(client):
    request = {
        "Request_ID": 263,
        "Withdrawal_Reason": ""
    }
    response = client.post("/api/wfh/requests/rejectwithdrawal", json=request)
    assert response.status_code == 500
    
def test_reject_withdrawal_success(client):
    request = {
        "Request_ID": 263,
        "Withdrawal_Reason": "test withdraw",
        "Manager_ID":151408,
        
    }
    response = client.post("/api/wfh/requests/rejectwithdrawal", json=request)
    assert response.status_code == 200
    
    