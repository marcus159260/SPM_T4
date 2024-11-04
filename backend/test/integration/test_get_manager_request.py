import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_requests_per_approver_success(client):
    # Test Philip Lee, role 1
    test_ID = 151408
    headers_data = {
        'X-Staff_ID': test_ID,
        'X-Staff-Role': 1
    }
    print(test_ID)
    response = client.get(f"/api/wfh/requests/approver/{test_ID}", headers=headers_data)
    assert response.status_code == 200
    
def test_get_requests_per_approver_fail(client):
    # Test Philip Lee, role 1
    test_ID = 157006
    headers_data = {
        'X-Staff_ID': test_ID,
        'X-Staff-Role': 2
    }
    print(test_ID)
    response = client.get(f"/api/wfh/requests/approver/{test_ID}", headers=headers_data)
    assert response.status_code == 403