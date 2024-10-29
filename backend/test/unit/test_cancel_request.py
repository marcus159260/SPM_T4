import pytest
from unittest.mock import MagicMock

from controllers.requests_controller import cancel_wfh_request

def test_request_invalid_requestid(mocker):
    # Mock Supabase table response for a non-existent request
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = []

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = cancel_wfh_request(request_id=1, reason="No longer needed", staff_id=140008)
    
    # Assertions
    assert result['error'] == 'Request not found.'
    assert result['status'] == 404


def test_unauthorized_access(mocker):
    # Mock Supabase table response for a request that belongs to a different staff member
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = cancel_wfh_request(request_id=1, reason="No longer needed", staff_id=140009)
    
    # Assertions
    assert result['error'] == 'Unauthorized'
    assert result['status'] == 403


def test_successful_cancellation(mocker):
    # Mock Supabase table response for an existing request
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mock update response
    mock_update_response = MagicMock()
    mock_update_response.data = None

    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_update_response

    # Run the function
    result = cancel_wfh_request(request_id=1, reason="No longer needed", staff_id=140008)
    
    # Assertions
    assert result['message'] == 'Request cancelled successfully.'
    assert result['status'] == 200


def test_general_exception_database(mocker):
    # Mock Supabase table to throw an exception
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_supabase.table.side_effect = Exception("Database connection failed")

    # Run the function
    result = cancel_wfh_request(request_id=1, reason="No longer needed", staff_id=140008)
    
    # Assertions
    assert result['error'] == "Database connection failed"
    assert result['status'] == 500


def test_general_exception_unsuccessful(mocker):
    # Mock Supabase table response for an existing request
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Simulate update failure
    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.side_effect = Exception("Update failed")

    # Run the function
    result = cancel_wfh_request(request_id=1, reason="No longer needed", staff_id=140008)
    
    # Assertions
    assert result['error'] == 'Update failed'
    assert result['status'] == 500