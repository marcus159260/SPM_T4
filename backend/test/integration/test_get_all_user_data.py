import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch
from routes.user_routes import user_bp

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_all_users_data_success(client):
    response = client.get('/api/users/')
    assert response.status_code == 200
    
@patch('routes.user_routes.get_all_users_data')
def test_get_all_users_data_fail(mock, client):
    # Simulate the function returning None, causing a 500 error
    mock.return_value = None

    response = client.get('/api/users/')
    print(response.data)
    assert response.status_code == 404

    
        