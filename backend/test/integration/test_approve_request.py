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
        
def test_role_required_allowed(client):
    headers = {'X-Staff-ID': '151408', 'X-Staff-Role': 1}  # Role is allowed
    response = client.post('/requests/approve', headers=headers, json={'Request_ID': 263, 'request_Status': 'Pending'})
    assert response.status_code == 200  # Assuming a successful response if role is allowed