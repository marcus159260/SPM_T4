import json
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from routes.requests import wfh_bp 


@pytest.fixture
def app():
    app = Flask(__name__)

    # Mocking the authentication decorators to allow all requests through
    with patch('routes.user_routes.login_required', lambda f: f), \
         patch('routes.user_routes.role_required', lambda roles: lambda f: f):
        app.register_blueprint(wfh_bp)
        yield app


@pytest.fixture
def client(app):
    with app.test_client() as client:
        # Set default headers for authentication
        client.environ_base['HTTP_X_STAFF_ID'] = '140008'  # Example staff ID
        client.environ_base['HTTP_X_STAFF_ROLE'] = '1'      # Example role
        yield client


def test_get_wfh_requests(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        mock_rpc.return_value.execute.return_value = ([None, [{'request_data': 'example data'}]], ['count'])

        response = client.get('/requests') 
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [{'request_data': 'example data'}]


def test_get_wfh_requests_error1(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        # Simulate an error condition from the RPC call
        mock_rpc.return_value.execute.return_value = (None, ['no data'])  # This is your error case
        response = client.get('/requests')
        assert response.status_code == 501  # Expecting a 501 status for error condition
        data = json.loads(response.data)
        assert data == {"error": "Error fetching data: ['no data']"}  


def test_get_wfh_requests_error2(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        # Simulating the `execute` method to raise an exception
        mock_rpc.return_value.execute.side_effect = Exception('Error fetching data')

        response = client.get('/requests')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {"error": "Error fetching data"} 


def test_get_staff_requests(client):
    with patch('routes.requests.get_staff_requests_data') as mock_get_staff_requests:
        mock_get_staff_requests.return_value = [{'id': 140008, 'status': 'Pending'}]

        response = client.get('/140008')
        print(f"Response Status Code: {response.status_code}")  # Debug print
        print(f"Response Data: {response.data}")  # Debug print
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == {"status": "success", "data": [{'id': 140008, 'status': 'Pending'}]}



def test_get_staff_requests_not_found(client):
    with patch('routes.requests.get_staff_requests_data') as mock_get_staff_requests:
        mock_get_staff_requests.return_value = None

        response = client.get('/140008')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {"status": "error", "message": "Requests for 140008 not found"}


def test_get_all_events(client):
    with patch('routes.requests.get_all_events_data') as mock_get_all_events:
        mock_get_all_events.return_value = [{'event': 'Team Building'}, {'event': 'Training'}]

        response = client.get('/all_events')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 2
        assert data==[{'event': 'Team Building'}, {'event': 'Training'}]


def test_get_all_events_no_data(client):
    with patch('routes.requests.get_all_events_data') as mock_get_all_events:
        mock_get_all_events.return_value = None

        response = client.get('/all_events')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data=={'error': 'Failed to fetch events data'}


def test_get_events_for_current_user_success(client):
    staff_id = 140008
    with patch('routes.requests.get_staff_events_data') as mock_get_events:
        mock_get_events.return_value = [{'event_id': 1, 'event_name': 'Team Meeting'}]

        response = client.get(f'/events/{staff_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert len(data) == 1
        assert data[0]['event_id'] == 1
        assert data[0]['event_name'] == 'Team Meeting'


def test_get_events_for_current_user_no_events(client):
    staff_id = 140008
    with patch('routes.requests.get_staff_events_data') as mock_get_events:
        mock_get_events.return_value = None  # Simulate no events found

        response = client.get(f'/events/{staff_id}')

        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {'error': 'Failed to fetch events data'}


def test_get_events_for_current_user_unauthorized(client):
    response = client.get('/events/0')  # Assuming staff_id should be a positive integer

    assert response.status_code == 401
    data = json.loads(response.data)
    assert data == {'error': 'Unauthorized'}


def test_get_user_req_success(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        mock_rpc.return_value.execute.return_value = type('MockResponse', (object,), {'data': [{'request_id': 1}], 'error': None})()

        response = client.get('/requests/140008')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data == [{'request_id': 1}]


def test_get_user_req_no_data(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        mock_rpc.return_value.execute.return_value = type('MockResponse', (object,), {'data': [], 'error': None})()

        response = client.get('/requests/140008')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {"error": "No data found"}


def test_get_user_req_error(client):
    with patch('util.db.supabase.rpc', side_effect=Exception("Database error")):
        response = client.get('/requests/140008')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {"error": "Database error"}


# def test_get_requests_by_approver_success(client):
#     with patch('util.db.supabase.rpc') as mock_rpc:
#         mock_rpc.return_value.execute.return_value = type('', (object,), {'data': [{'id': 1, 'status': 'Pending'}]})()

#         response = client.get('/requests/approver/140008')
#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data == [{'id': 1, 'status': 'Pending'}]


def test_get_requests_by_approver_sql_error(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        # Set up the return value to mimic an error in the data structure
        mock_rpc.return_value.execute.return_value = type('', (object,), {'data': [{'Error': 'SQL error in RPC function'}]})()

        response = client.get('/requests/approver/140008')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data == {'error': 'SQL error in RPC function'}


def test_get_requests_by_approver_exception(client):
    with patch('util.db.supabase.rpc') as mock_rpc:
        # Simulate an exception raised during the RPC call
        mock_rpc.side_effect = Exception("Unexpected error")

        response = client.get('/requests/approver/140008')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data == {'error': 'Unexpected error'}


# def test_create_request(client):
#     with patch('routes.requests.check_conflict') as mock_check_conflict, \
#          patch('util.db.supabase.rpc') as mock_rpc:
#         mock_check_conflict.return_value.data = 'No conflict'
#         mock_rpc.return_value.execute.return_value = {'data': [{'first_request_id': 1, 'message': 'Request created successfully'}], 'error': None}

#         request_data = {
#             'staff_id': 140008,
#             'start_date': '2024-10-30',
#             'end_date': '2024-11-05',
#             'time_of_day': 'Full Day',
#             'request_type': 'Work from Home',
#             'status': 'Pending',
#             'reason': 'Medical Appointment',
#             'approver_id': 1,
#             'requested_dates': ['2024-10-30']
#         }

#         response = client.post('/requests', json=request_data)

#         assert response.status_code == 201
#         data = json.loads(response.data)
#         assert data['first_request_id'] == 1
#         assert data['message'] == 'Request created successfully'


# def test_create_request_conflict(client):
#     with patch('routes.requests.check_conflict') as mock_check_conflict:
#         mock_check_conflict.return_value.data = 'Conflict found'

#         request_data = {
#             'staff_id': 140008,
#             'start_date': '2024-10-30',
#             'end_date': '2024-11-05',
#             'time_of_day': 'Full Day',
#             'request_type': 'Work from Home',
#             'status': 'Pending',
#             'reason': 'Medical Appointment',
#             'approver_id': 1,
#             'requested_dates': ['2024-10-30']
#         }

#         response = client.post('/requests', json=request_data)

#         assert response.status_code == 400
#         data = json.loads(response.data)
#         assert data['error'] == 'Conflict found'


# def test_withdraw_request(client):
#     with patch('routes.requests.withdraw_request_controller') as mock_withdraw:
#         mock_withdraw.return_value = {'status': 'success'}, 200

#         request_data = {
#             'Request_ID': 1,
#             'Rejection_Reason': 'Changed my mind',
#             'Staff_ID': 140008
#         }

#         response = client.post('/requests/withdraw', json=request_data)

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['status'] == 'success'


# def test_withdraw_request_missing_fields(client):
#     request_data = {
#         'Request_ID': 1,
#         # Missing Rejection_Reason and Staff_ID
#     }

#     response = client.post('/requests/withdraw', json=request_data)

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert data['error'] == 'Request ID and reason are required.'


# def test_cancel_request(client):
#     with patch('routes.requests.cancel_wfh_request') as mock_cancel:
#         mock_cancel.return_value = {'status': 200}, 200

#         request_data = {
#             'Request_ID': 1,
#             'Withdrawal_Reason': 'Changed my mind',
#             'Staff_ID': 140008
#         }

#         response = client.post('/requests/cancel', json=request_data)

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['status'] == 200


# def test_cancel_request_missing_fields(client):
#     request_data = {
#         'Request_ID': 1,
#         # Missing Withdrawal_Reason and Staff_ID
#     }

#     response = client.post('/requests/cancel', json=request_data)

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert data['error'] == 'Request ID and reason are required.'


# def test_approve_request(client):
#     with patch('routes.requests.approve_wfh_request') as mock_approve:
#         mock_approve.return_value = {'status': 'success'}, 200

#         request_data = {
#             'Request_ID': 1,
#             'request_Status': 'Approved'
#         }

#         response = client.post('/requests/approve', json=request_data)

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['status'] == 'success'


# def test_approve_request_missing_fields(client):
#     request_data = {
#         # Missing Request_ID and request_Status
#     }

#     response = client.post('/requests/approve', json=request_data)

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert data['error'] == 'Missing request ID or status'


# def test_reject_request(client):
#     with patch('routes.requests.reject_wfh_request') as mock_reject:
#         mock_reject.return_value = {'status': 'success'}, 200

#         request_data = {
#             'Request_ID': 1,
#             'Rejection_Reason': 'Not applicable',
#             'Staff_ID': 140008
#         }

#         response = client.post('/requests/reject', json=request_data)

#         assert response.status_code == 200
#         data = json.loads(response.data)
#         assert data['status'] == 'success'


# def test_reject_request_missing_fields(client):
#     request_data = {
#         'Request_ID': 1,
#         # Missing Rejection_Reason and Staff_ID
#     }

#     response = client.post('/requests/reject', json=request_data)

#     assert response.status_code == 400
#     data = json.loads(response.data)
#     assert data['error'] == 'Missing request ID or rejection reason.'