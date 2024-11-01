import json
import pytest
from flask import Flask
from unittest.mock import patch
from routes.user_routes import user_bp 
# Create a test Flask app
@pytest.fixture
def app():
    app = Flask(__name__)
    # Mocking the authentication decorators to allow all requests through
    with patch('routes.user_routes.login_required', lambda f: f), \
         patch('routes.user_routes.role_required', lambda roles: lambda f: f):
        app.register_blueprint(user_bp)
        yield app
@pytest.fixture
def client(app):
    with app.test_client() as client:
        # Set default headers for authentication
        client.environ_base['HTTP_X_STAFF_ID'] = '140008'  # Example staff ID
        client.environ_base['HTTP_X_STAFF_ROLE'] = '1'      # Example role
        yield client
# def test_users_success(client):
#     with patch('routes.user_routes.get_all_users_names') as mock_get_all_users:
#         mock_get_all_users.return_value = ['Alice', 'Bob']
        
#         response = client.get('/')
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data == ['Alice', 'Bob']
# def test_users_not_found(client):
#     with patch('routes.user_routes.get_all_users_names') as mock_get_all_users:
#         mock_get_all_users.return_value = None
        
#         response = client.get('/')
#         assert response.status_code == 404
#         data = json.loads(response.data)
#         assert data == {'error': 'Users not found'}
# def test_get_all_users(client):
#     with patch('routes.user_routes.get_all_users_data') as mock_get_all_users_data:
#         mock_get_all_users_data.return_value = [{'name': 'Alice'}, {'name': 'Bob'}]
        
#         response = client.get('/')
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data == {"status": "success", "data": [{'name': 'Alice'}, {'name': 'Bob'}]}
# def test_get_all_users_no_data(client):
#     with patch('routes.user_routes.get_all_users_data') as mock_get_all_users_data:
#         mock_get_all_users_data.return_value = None
        
#         response = client.get('/')
#         assert response.status_code == 404
#         data = json.loads(response.data)
#         assert data == {"status": "error", "message": "No data found"}
def test_get_user_by_id(client):
    user_id = 140001
    with patch('routes.user_routes.get_user_data_by_id') as mock_get_user:
        mock_get_user.return_value = {'id': user_id, 'name': 'Alice'}
        response = client.get(f'/{user_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"status": "success", "data": {'id': user_id, 'name': 'Alice'}}
def test_get_user_by_id_not_found(client):
    user_id = 140001
    with patch('routes.user_routes.get_user_data_by_id') as mock_get_user:
        mock_get_user.return_value = None
        response = client.get(f'/{user_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data == {"status": "error", "message": "User not found"}
def test_get_manager_details(client):
    manager_id = 140001
    with patch('routes.user_routes.get_manager_details_data') as mock_get_manager:
        mock_get_manager.return_value = {'id': manager_id, 'name': 'Manager Alice'}
        response = client.get(f'/get-manager/{manager_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"status": "success", "data": {'id': manager_id, 'name': 'Manager Alice'}}
def test_get_manager_details_not_found(client):
    manager_id = 140001
    with patch('routes.user_routes.get_manager_details_data') as mock_get_manager:
        mock_get_manager.return_value = None
        response = client.get(f'/get-manager/{manager_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data == {"status": "error", "message": "User not found"}
def test_get_employees_by_dept(client):
    with patch('routes.user_routes.get_employees_by_dept_data') as mock_get_employees:
        mock_get_employees.return_value = [{'name': 'Alice'}, {'name': 'Bob'}]
        response = client.get('/by-dept-employees')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"status": "success", "data": [{'name': 'Alice'}, {'name': 'Bob'}]}
def test_get_employees_by_dept_not_found(client):
    with patch('routes.user_routes.get_employees_by_dept_data') as mock_get_employees:
        mock_get_employees.return_value = None
        response = client.get('/by-dept-employees')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data == {"status": "error", "message": "User not found"}
def test_get_resources_endpoint(client):
    with patch('routes.user_routes.get_resources') as mock_get_resources:
        mock_get_resources.return_value = {'resource1': 'data1', 'resource2': 'data2'}
        response = client.get('/resources', headers={'X-Staff-ID': '140008', 'X-Staff-Role': '1'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {'resource1': 'data1', 'resource2': 'data2'}
def test_get_resources_endpoint_failure(client):
    with patch('routes.user_routes.get_resources') as mock_get_resources:
        mock_get_resources.return_value = None
        response = client.get('/resources', headers={'X-Staff-ID': '140008', 'X-Staff-Role': '1'})
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {'error': 'Failed to fetch employee data'}
def test_get_employees_by_team(client):
    reporting_manager_id = 140894
    with patch('routes.user_routes.get_employees_by_reporting_manager') as mock_get_employees:
        mock_get_employees.return_value = [
            {'Staff_FName': 'Alice', 'Staff_LName': 'Smith', 'Staff_ID': '1', 'Dept': 'HR', 'Position': 'Manager'},
            {'Staff_FName': 'Bob', 'Staff_LName': 'Johnson', 'Staff_ID': '2', 'Dept': 'IT', 'Position': 'Developer'}
        ]
        response = client.get(f'/by-team-employees/{reporting_manager_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {
            "status": "success",
            "data": [
                {"name": "Alice Smith", "id": "1", "Dept": "HR", "Position": "Manager"},
                {"name": "Bob Johnson", "id": "2", "Dept": "IT", "Position": "Developer"}
            ]
        }
def test_get_employees_by_team_not_found(client):
    reporting_manager_id = 140894
    with patch('routes.user_routes.get_employees_by_reporting_manager') as mock_get_employees:
        mock_get_employees.return_value = []
        response = client.get(f'/by-team-employees/{reporting_manager_id}')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data == {"status": "error", "message": "User not found"}