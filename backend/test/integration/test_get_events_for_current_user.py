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

    
def test_get_current_user_events_success(client):
    test_ID = 150076
    response = client.get(f'/api/wfh/events/{test_ID}')
    print(response.data)
    assert response.status_code == 200
    
def test_get_current_user_events_404(client):
    staff_ID_value = None
    response = client.get(f'/api/wfh/events/{staff_ID_value}')
    response_json = response.get_json()

    # assert response_json['error'] == 'Unauthorized'
    assert response.status_code == 404
    
    
@patch('routes.requests.get_staff_events_data')      
def test_get_current_user_events_valid_user_but_no_events(mock, client):
    mock.return_value = None
    response = client.get(f'/api/wfh/events/{150076}')
    print(response.data)
    assert response.get_json()['error'] =='Failed to fetch events data'
    assert response.status_code == 500
    