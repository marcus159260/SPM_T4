import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch, MagicMock
from controllers.user_controller import get_department_wfh_wfo_counts
# from controllers import user_controller
from routes.user_routes import user_bp

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('routes.requests.get_all_events_data')       
def test_get_all_events_fail(mock, client):
    mock.return_value = None
    response = client.get('/api/wfh/all_events')
    print(response.data)
    assert response.status_code == 500  
    
@patch('routes.requests.get_all_events_data')      
def test_get_all_events_success(mock, client):
    mock.return_value = True
    response = client.get('/api/wfh/all_events')
    print(response.data)
    assert response.status_code == 200  
    