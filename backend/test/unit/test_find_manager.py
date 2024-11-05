import pytest
from unittest.mock import MagicMock
from controllers.user_controller import find_manager_details_data

def test_find_manager_details_data_manager_found(mocker):
    # Arrange: Mock the Supabase client to simulate a response with manager data
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = [{'Reporting_Manager': 'Manager1'}]

    # Act: Call the function with a sample staff ID
    result = find_manager_details_data(140008)

    # Assert: Check that the correct data is returned
    assert result == {'Reporting_Manager': 'Manager1'}
    mock_supabase.table.assert_called_once_with('employee')
    mock_supabase.table.return_value.select.assert_called_once_with('Reporting_Manager')
    mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('Staff_ID', 140008)

def test_find_manager_details_data_no_manager(mocker):
    # Arrange: Mock the Supabase client to simulate an empty response (no manager found)
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []

    # Act: Call the function with a sample staff ID
    result = find_manager_details_data(140008)

    # Assert: Check that None is returned when no manager is found
    assert result is None
    mock_supabase.table.assert_called_once_with('employee')
    mock_supabase.table.return_value.select.assert_called_once_with('Reporting_Manager')
    mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('Staff_ID', 140008)
