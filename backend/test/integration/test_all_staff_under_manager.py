import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_by_team_success(client):
    test_ID = 140001
    response = client.get(f'/api/users/all-staff-under-manager/{test_ID}')
    assert response.status_code == 200
    
def test_get_invalid_reporting_mgr_id(client):
    test_ID = 00000 #Non-existing staff
    response = client.get(f'/api/users/all-staff-under-manager/{test_ID}')
    assert response.status_code == 404
