import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_manager_details_success(client):
    test_ID = 151408
    response = client.get(f"/api/users/get-manager/{test_ID}")
    assert response.status_code == 200
    
def test_get_manager_details_fail_not_found(client):
    test_ID = 000000
    response = client.get(f"/api/users/get-manager/{test_ID}")
    assert response.status_code == 404
    
    
    
    

        