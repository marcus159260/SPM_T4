import pytest
import json
from app import app 
from util.db import supabase

#NEED TO ADD LOGIN FIRST (not done)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client
        
def test_get_department_counts_success(client):
    response = client.get('/api/users/department_counts')
    assert response.status_code == 200