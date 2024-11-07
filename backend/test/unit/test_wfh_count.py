import pytest
from unittest.mock import MagicMock
from datetime import datetime
from controllers.requests_controller import get_wfh_count  

@pytest.fixture
def mock_supabase(mocker):
    return mocker.patch('controllers.requests_controller.supabase')

def test_get_wfh_count_with_valid_requests(mock_supabase):
    # Mock response with approved requests for the specified date
    mock_response = MagicMock()
    mock_response.data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
    ]
    mock_supabase.table().select().eq().eq().eq().execute.return_value = mock_response
    
    count = get_wfh_count('123', '2023-11-05')

    # Verify that the count of approved requests matches the expected value
    assert count == 2

def test_get_wfh_count_no_approved_requests(mock_supabase):
    # Mock response with no approved requests for the specified date
    mock_response = MagicMock()
    mock_response.data = []  # No matching requests
    mock_supabase.table().select().eq().eq().eq().execute.return_value = mock_response
    
    count = get_wfh_count('123', '2023-11-05')

    # Verify that the function returns 0 when there are no approved requests
    assert count == 0


def test_get_wfh_count_exception_handling(mock_supabase):
    # Simulate an exception being raised during the request
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = Exception("Database error")

    count = get_wfh_count('123', '2023-11-05')

    # Verify that the function returns 0 on exception
    assert count == 0


def test_get_wfh_count_with_multiple_start_dates(mock_supabase):
    # Create a mock response with multiple start dates
    mock_data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-06'},
        {'Request_ID': 3, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-07'},
        {'Request_ID': 4, 'Approver_ID': '123', 'Status': 'Rejected', 'Start_Date': '2023-11-05'},
        {'Request_ID': 5, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
    ]

    # Mock the execute method to filter the mock data based on the function logic
    def mock_execute():
        return MagicMock(data=[request for request in mock_data
                                if request['Approver_ID'] == '123' and
                                request['Status'] == 'Approved' and
                                request['Start_Date'] == '2023-11-05'])

    # Set the mock execute function
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = mock_execute

    count = get_wfh_count('123', '2023-11-05')
    assert count == 2  # This should match the expected count based on the filtering logic

def test_get_wfh_count_with_multiple_statuses(mock_supabase):
    # Create a mock response with multiple statuses
    mock_data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '123', 'Status': 'Rejected', 'Start_Date': '2023-11-05'},
        {'Request_ID': 3, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-06'},
        {'Request_ID': 4, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 5, 'Approver_ID': '123', 'Status': 'Pending', 'Start_Date': '2023-11-05'},
    ]

    # Mock the execute method to filter the mock data based on the function logic
    def mock_execute():
        return MagicMock(data=[request for request in mock_data
                                if request['Approver_ID'] == '123' and
                                request['Status'] == 'Approved' and
                                request['Start_Date'] == '2023-11-05'])

    # Set the mock execute function
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = mock_execute

    count = get_wfh_count('123', '2023-11-05')
    assert count == 2  # This should match the expected count based on the filtering logic

def test_get_wfh_count_no_requests_with_multiple_statuses(mock_supabase):
    # Create a mock response with no matching requests
    mock_data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Rejected', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '123', 'Status': 'Pending', 'Start_Date': '2023-11-06'},
    ]

    # Mock the execute method to filter the mock data
    def mock_execute():
        return MagicMock(data=[request for request in mock_data
                                if request['Approver_ID'] == '123' and
                                request['Status'] == 'Approved' and
                                request['Start_Date'] == '2023-11-05'])

    # Set the mock execute function
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = mock_execute

    count = get_wfh_count('123', '2023-11-05')
    assert count == 0  # No matching requests

def test_get_wfh_count_with_different_dates(mock_supabase):
    # Create a mock response with different dates
    mock_data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-06'},
        {'Request_ID': 3, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-07'},
    ]

    # Mock the execute method to filter the mock data
    def mock_execute():
        return MagicMock(data=[request for request in mock_data
                                if request['Approver_ID'] == '123' and
                                request['Status'] == 'Approved' and
                                request['Start_Date'] == '2023-11-06'])

    # Set the mock execute function
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = mock_execute

    count = get_wfh_count('123', '2023-11-06')
    assert count == 1  # Only one request matches the date and status criteria


def test_get_wfh_count_with_different_managerid(mock_supabase):
    # Create a mock response with different dates
    mock_data = [
        {'Request_ID': 1, 'Approver_ID': '123', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 2, 'Approver_ID': '12', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
        {'Request_ID': 3, 'Approver_ID': '1234', 'Status': 'Approved', 'Start_Date': '2023-11-05'},
    ]

    # Mock the execute method to filter the mock data
    def mock_execute():
        return MagicMock(data=[request for request in mock_data
                                if request['Approver_ID'] == '123' and
                                request['Status'] == 'Approved' and
                                request['Start_Date'] == '2023-11-05'])

    # Set the mock execute function
    mock_supabase.table().select().eq().eq().eq().execute.side_effect = mock_execute

    count = get_wfh_count('123', '2023-11-05')
    assert count == 1  # Only one request matches the date and status criteria