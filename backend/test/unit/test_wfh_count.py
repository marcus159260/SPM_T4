import pytest
from unittest.mock import MagicMock

from controllers.requests_controller import get_wfh_count

def test_get_wfh_count_no_requests(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for no approved requests
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.lte.return_value.gte.return_value.execute.return_value = mock_response

    # Run the function
    count = get_wfh_count(requested_date='2024-10-28')

    # Assertions
    assert count == 0  # Expecting 0 when no requests are approved


def test_get_wfh_count_all_approved(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for some approved requests
    mock_response = MagicMock()
    mock_response.data = [
        {'Request_ID': 4, 'Status': 'Approved', 'Start_Date': '2024-10-28', 'End_Date': '2024-10-28'},
        {'Request_ID': 5, 'Status': 'Approved', 'Start_Date': '2024-10-28', 'End_Date': '2024-10-28'},
        {'Request_ID': 7, 'Status': 'Approved', 'Start_Date': '2024-10-28', 'End_Date': '2024-10-28'},
        {'Request_ID': 10, 'Status': 'Approved', 'Start_Date': '2024-10-28', 'End_Date': '2024-10-28'},
        {'Request_ID': 13, 'Status': 'Approved', 'Start_Date': '2024-10-28', 'End_Date': '2024-10-28'}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.lte.return_value.gte.return_value.execute.return_value = mock_response

    # Run the function
    count = get_wfh_count(requested_date='2024-10-28')

    # Assertions
    assert count == 5  # Expecting 5 approved requests


def test_get_wfh_count_with_exception(mocker, capfd):
    # Mock the Supabase client to raise an exception
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_supabase.table.return_value.select.return_value.eq.return_value.lte.return_value.gte.return_value.execute.side_effect = Exception("Database error")

    # Run the function, which should now raise the mocked exception
    count = get_wfh_count(requested_date='2024-10-28')

    # Capture the output
    captured = capfd.readouterr()

    # Assertions
    assert count == 0  # Expecting 0 because of the exception
    assert "Error retrieving WFH count: Database error" in captured.out  # Check the printed output
