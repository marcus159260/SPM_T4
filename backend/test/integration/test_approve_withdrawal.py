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
        
def test_approve_withdrawal_success(client):
    request = {
        "Request_ID": 263,
        "Manager_ID": 151408
    }
    response = client.post("/api/wfh/requests/approvewithdrawal", json=request)
    assert response.status_code == 200
    
def test_approve_withdrawal_no_requestid_fail(client):
    request = {
    }
    response = client.post("/api/wfh/requests/approvewithdrawal", json=request)
    assert response.status_code == 400
    
@patch('routes.requests.approve_withdrawal_wfh_request') 
def test_approve_withdrawal_500_fail(mock,client):
    mock.return_value = 500
    response = client.post("/api/wfh/requests/approvewithdrawal")
    assert response.status_code == 500
    
    