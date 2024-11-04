import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from controllers.requests_controller import approve_wfh_request

def test_request_invalid_requestid(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    
    # Mock response for non-existent request
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = approve_wfh_request(managerId=1, request_id=1, status='Approved')

    # Assertions
    assert result['error'] == 'Request not found.'
    assert result['status'] == 404


def test_approve_future_request_valid(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for an existing request
    mock_response = MagicMock()
    mock_response.data = [{
        'Request_ID': 1,
        'Application_Date': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        'Start_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        'End_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mocking the get_total_office_strength and get_wfh_count
    mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
    mocker.patch('controllers.requests_controller.get_wfh_count', return_value=4)

    # Run the function
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Pending')

    # Assertions
    assert result['message'] == "Request approved successfully."
    assert status_code == 200  


def test_approve_future_request_violation(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for an existing request
    mock_response = MagicMock()
    mock_response.data = [{
        'Request_ID': 1,
        'Application_Date': (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        'Start_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"),
        'End_Date': (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mocking the get_total_office_strength and get_wfh_count
    mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
    mocker.patch('controllers.requests_controller.get_wfh_count', return_value=5)

    # Run the function
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Pending')

    # Assertions
    assert result['error'] == 'Cannot approve request as less than 50% of the team will be in the office.'
    assert status_code == 400


def test_approve_past_request_valid(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for an existing request
    mock_response = MagicMock()
    mock_response.data = [{
        'Request_ID': 1,
        'Application_Date': (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        'Start_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        'End_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mocking the get_total_office_strength and get_wfh_count
    mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
    mocker.patch('controllers.requests_controller.get_wfh_count', return_value=4)

    # Run the function
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Pending')

    # Assertions
    assert result['message'] == "Request approved successfully."
    assert status_code == 200  


def test_approve_past_request_force_approval(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for an existing request
    mock_response = MagicMock()
    mock_response.data = [{
        'Request_ID': 1,
        'Application_Date': (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        'Start_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        'End_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mocking the get_total_office_strength and get_wfh_count
    mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
    mocker.patch('controllers.requests_controller.get_wfh_count', return_value=6)

    # Run the function with force approval
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Pending', force_approval=True)

    # Assertions
    assert result['message'] == "Request approved successfully despite policy violation."
    assert status_code == 200  


def test_approve_past_request_not_force_approval(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for an existing request
    mock_response = MagicMock()
    mock_response.data = [{
        'Request_ID': 1,
        'Application_Date': (datetime.now() - timedelta(days=10)).strftime("%Y-%m-%d"),
        'Start_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
        'End_Date': (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Mocking the get_total_office_strength and get_wfh_count
    mocker.patch('controllers.requests_controller.get_total_office_strength', return_value=10)
    mocker.patch('controllers.requests_controller.get_wfh_count', return_value=6)

    # Run the function without force approval
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Pending', force_approval=False)

    # Assertions
    assert result['error'] == 'Violation of 50% WFH policy for backdated request'
    assert status_code == 409


def test_exception_handling(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response to throw an exception
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

    # Run the function
    result, status_code = approve_wfh_request(managerId=1, request_id=1, status='Approved')

    # Assertions
    assert result['error'] == 'Database error'
    assert status_code == 500
