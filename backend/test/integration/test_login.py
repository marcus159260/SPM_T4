import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
        
def test_login_success(client):
    request = {"Staff_ID": 150076}
    response = client.post('/api/auth/login', json=request)
    assert response.status_code == 200
    
def test_login_fail(client):
    request = {"Staff_ID": "wfhqueen"}
    response = client.post('/api/auth/login', json=request)
    assert response.status_code == 401
    

    
    