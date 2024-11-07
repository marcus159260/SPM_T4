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
        
def test_get_department_counts_success(client):
    response = client.get('/api/users/department_counts')
    assert response.status_code == 200
    
    
@patch('routes.user_routes.get_department_wfh_wfo_counts')
def test_get_department_counts_500(mock_get_counts, client):
    # Simulate the function returning None, causing a 500 error
    mock_get_counts.return_value = None

    response = client.get('/api/users/department_counts')
    print(response.data)
    assert response.status_code == 500
