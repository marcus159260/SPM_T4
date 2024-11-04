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
    headers = {
        "X-Staff_ID": test_ID,
        "X-Staff-Role": 1
    }
    response = client.get(f"/api/requests/approver/${test_ID}", headers=headers)
    assert response == 200