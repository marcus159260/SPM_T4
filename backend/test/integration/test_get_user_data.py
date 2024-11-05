import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_user_data_valid_id(client):
    test_ID = 150076
    response = client.get(f"/api/users/{test_ID}")
    assert response.status_code == 200
    
def test_get_user_data_valid_id(client):
    test_ID = 000000
    response = client.get(f"/api/users/{test_ID}")
    assert response.status_code == 404    
    