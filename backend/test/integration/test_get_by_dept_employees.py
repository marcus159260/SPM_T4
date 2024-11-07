import pytest
import json
from app import app 
from util.db import supabase
from unittest.mock import patch
from routes.user_routes import user_bp

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_by_dept_employees_success(client):
    response = client.get('/api/users/by-dept-employees')
    assert response.status_code == 200    
    

@patch('routes.user_routes.get_employees_by_dept_data')   
def test_get_by_dept_employees_fail(mock, client):
    mock.return_value = False
    response = client.get('/api/users/by-dept-employees')
    assert response.status_code == 404 