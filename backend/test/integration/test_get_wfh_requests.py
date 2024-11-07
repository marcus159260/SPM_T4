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
            
def test_get_requests_success(client):
    response = client.get('/api/wfh/requests', query_string={'managerId': 151408})
    assert response.status_code == 200
 
@patch('util.db.supabase.rpc')     
def test_get_requests_fail(mock_rpc, client):
    mock_response = MagicMock()
    mock_response.execute.return_value = (None, ['error'])
    
    mock_rpc.return_value = mock_response
    response = client.get('/api/wfh/requests', query_string={'managerId': 151408})
    print(response)
    assert response.status_code == 501
    
@patch('util.db.supabase.rpc')    
def test_get_requests_500(mock_rpc, client):
    mock_response = MagicMock()
    mock_response.execute.side_effect = Exception("Internal Server Error")
    
    mock_rpc.return_value = mock_response
    response = client.get('/api/wfh/requests', query_string={'managerId': 151408})
    print(response)
    assert response.status_code == 500
    