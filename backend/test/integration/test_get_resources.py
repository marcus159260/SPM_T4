import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch
from controllers.user_controller import get_department_wfh_wfo_counts
# from controllers import user_controller
from routes.user_routes import user_bp

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

      
def test_get_resources_success(client):
    
    headers_data = {
        "X-Staff-ID": 130002,
        "X-Staff_Role":1 
    }
    
    response = client.get('/api/users/resources', headers=headers_data)
    print(response.data)
    assert response != None
    
@patch('routes.user_routes.get_resources')       
def test_get_resources_fail(mock, client):
    
    headers_data = {
        "X-Staff-ID": 130002,
        "X-Staff_Role":1 
    }
    
    mock.return_value = None
    response = client.get('/api/users/resources', headers=headers_data)
    print(response.data)
    assert response.status_code == 500
