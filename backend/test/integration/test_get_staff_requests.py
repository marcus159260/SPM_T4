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
        
def test_get_staff_requests_success(client):
    response = client.get(f"/api/wfh/{150076}")
    assert response.status_code == 200
    
def test_get_staff_requests_fail(client):
    response = client.get(f"/api/wfh/{000000}")
    assert response.status_code == 404
