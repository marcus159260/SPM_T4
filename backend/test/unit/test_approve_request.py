import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from controllers.requests_controller import approve_wfh_request

def test_request_not_found(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    
    # Mock response for non-existent request
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = approve_wfh_request(request_id=999, status='Approved')

    # Assertions
    assert result['error'] == 'Request not found.'
    assert result['status'] == 404

# def test_approve_future_request_valid(mocker):
#     # Mock the Supabase client
#     mock_supabase = mocker.patch('controllers.requests_controller.supabase')

#     # Mock response for an existing request
#     mock_response = MagicMock()
#     mock_response.data = [{
#         'Request_ID': 1,
#         'Application_Date': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
#         'Start_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
#         'End_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
#     }]
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

#     # Mocking the get_total_office_strength and get_wfh_count
#     mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
#     mocker.patch('controllers.requests_controller.get_wfh_count', return_value=4)

#     # Run the function
#     result = approve_wfh_request(request_id=1, status='Approved')

#     # Assertions
#     assert result['message'] == "Request approved successfully."
#     assert result[1] == 200  # HTTP status code

# def test_approve_future_request_violation(mocker):
#     # Mock the Supabase client
#     mock_supabase = mocker.patch('controllers.requests_controller.supabase')

#     # Mock response for an existing request
#     mock_response = MagicMock()
#     mock_response.data = [{
#         'Request_ID': 1,
#         'Application_Date': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
#         'Start_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
#         'End_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
#     }]
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

#     # Mocking the get_total_office_strength and get_wfh_count
#     mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
#     mocker.patch('controllers.requests_controller.get_wfh_count', return_value=5)

#     # Run the function
#     result = approve_wfh_request(request_id=1, status='Approved')

#     # Assertions
#     assert result['error'] == 'Cannot approve request as less than 50% of the team will be in the office.'
#     assert result['status'] == 400

# def test_approve_past_request_valid(mocker):
#     # Mock the Supabase client
#     mock_supabase = mocker.patch('controllers.requests_controller.supabase')

#     # Mock response for an existing request
#     mock_response = MagicMock()
#     mock_response.data = [{
#         'Request_ID': 1,
#         'Application_Date': (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
#         'Start_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
#         'End_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
#     }]
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

#     # Mocking the get_total_office_strength and get_wfh_count
#     mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
#     mocker.patch('controllers.requests_controller.get_wfh_count', return_value=4)

#     # Run the function
#     result = approve_wfh_request(request_id=1, status='Approved')

#     # Assertions
#     assert result['message'] == "Request approved successfully."
#     assert result[1] == 200  # HTTP status code

# def test_approve_past_request_force_approval(mocker):
#     # Mock the Supabase client
#     mock_supabase = mocker.patch('controllers.requests_controller.supabase')

#     # Mock response for an existing request
#     mock_response = MagicMock()
#     mock_response.data = [{
#         'Request_ID': 1,
#         'Application_Date': (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
#         'Start_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
#         'End_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
#     }]
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

#     # Mocking the get_total_office_strength and get_wfh_count
#     mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
#     mocker.patch('controllers.requests_controller.get_wfh_count', return_value=6)

#     # Run the function with force approval
#     result = approve_wfh_request(request_id=1, status='Approved', force_approval=True)

#     # Assertions
#     assert result['message'] == "Request approved successfully despite policy violation."
#     assert result[1] == 200  # HTTP status code

# def test_exception_handling(mocker):
#     # Mock the Supabase client
#     mock_supabase = mocker.patch('controllers.requests_controller.supabase')

#     # Mock response to throw an exception
#     mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

#     # Run the function
#     result = approve_wfh_request(request_id=1, status='Approved')

#     # Assertions
#     assert result['error'] == 'Database error'
#     assert result[0] == 500  # HTTP status code