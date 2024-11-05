import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_user_request_success(client):
    test_ID = 150076
    response = client.get(f"/api/wfh/requests/{test_ID}")
    assert response.status_code == 200
    
# def test_get_user_request_fail(client):
#     test_ID = 123654
#     response = client.get(f"/api/wfh/requests/{test_ID}")
#     print(response)
#     assert response.status_code == 404
    
    