import json
import pytest
from flask import Flask
from unittest.mock import patch
from routes.auth import auth_bp 
# Create a test Flask app
@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_login_success(client):
    # Mock the authenticate_user function
    with patch('routes.auth.authenticate_user') as mock_authenticate:
        mock_authenticate.return_value = {'Staff_ID': '140008', 'name': 'Jaclyn Lee'}
        response = client.post('/login', json={'Staff_ID': '140008'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert data['user'] == {'Staff_ID': '140008', 'name': 'Jaclyn Lee'}


def test_login_failure(client):
    # Mock the authenticate_user function
    with patch('routes.auth.authenticate_user') as mock_authenticate:
        mock_authenticate.return_value = None
        response = client.post('/login', json={'Staff_ID': '140008'})
        
        assert response.status_code == 401
        data = json.loads(response.data)
        assert data['success'] is False
        assert data['message'] == 'Invalid username or password'