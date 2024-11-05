import pytest
import json
from app import app 
from util.db import supabase

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_by_dept_employees(client):
    response = client.get('/api/users/by-dept-employees')
    assert response.status_code == 200    