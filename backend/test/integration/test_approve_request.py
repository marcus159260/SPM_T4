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
        
def test_approve_request_allowed(client):
    request = {
        "managerId": 151408,
        "Request_ID": 263,
        "request_Status":"Approved" 
    }
    response = client.post('/api/wfh/requests/approve', headers=headers, json=request)
    assert response.status_code == 200  
    
