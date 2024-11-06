import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch, MagicMock

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_approve_request_allowed(client):
    request = {
        "managerId": 151408,
        "Request_ID": 263,
        "request_Status":"Approved" 
    }
    response = client.post('/api/wfh/requests/approve', json=request)
    assert response.status_code == 200  
    
def test_approve_request_no_request_id(client):
    request = {
        "managerId": 151408,
        "request_Status":"Approved" 
    }
    response = client.post('/api/wfh/requests/approve', json=request)
    assert response.status_code == 400  
    
def test_approve_request_no_request_status(client):
    request = {
        "managerId": 151408,
        "Request_ID": 263
    }
    response = client.post('/api/wfh/requests/approve', json=request)
    assert response.status_code == 400  
    
    
@patch('util.db.supabase.rpc')    
def test_get_requests_500(mock_rpc, client):
    mock_response = MagicMock()
    mock_response.execute.side_effect = Exception("Internal Server Error")
    
    mock_rpc.return_value = mock_response
    request = {
        "managerId": 151408,
        "Request_ID": 263,
        "request_Status": "Approved"
    }
    response = client.post('/api/wfh/requests/approve', json=request)
    print(response)
    assert response.status_code == 500
    

    
