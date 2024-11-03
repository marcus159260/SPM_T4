#ignore this file for now
import pytest
from flask import session
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_required(client):
    response = client.get('/api/employee/dashboard')
    assert response.status_code == 401
    assert response.get_json() == {'error': 'Authentication required'}

def test_login_required_authenticated(client):
    with client.session_transaction() as sess:
        sess['staff_id'] = 150076
        sess['staff_fname'] = 'Oliver'
    response = client.get('/api/employee/dashboard')
    assert response.status_code == 200
    assert 'Welcome to your dashboard, Oliver!' in response.get_data(as_text=True)

def test_role_required_forbidden(client):
    with client.session_transaction() as sess:
        sess['staff_id'] = 150076
        sess['role'] = 'Staff'
    response = client.get('/api/employee/admin')
    assert response.status_code == 403
    assert response.get_json() == {'error': 'Forbidden'}

def test_role_required_authorized(client):
    with client.session_transaction() as sess:
        sess['staff_id'] = 150076
        sess['role'] = 'Admin'
    response = client.get('/api/employee/admin')
    assert response.status_code == 200
    assert 'Welcome to the admin panel' in response.get_data(as_text=True)