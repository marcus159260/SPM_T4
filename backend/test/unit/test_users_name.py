import pytest
from unittest.mock import MagicMock
from controllers.user_controller import get_all_users_names
def test_get_all_users_names(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    # Mock response for getting all users' names
    mock_response = MagicMock()
    mock_response.data = [
        {'Staff_ID': 1, 'Staff_FName': 'Jaclyn', 'Staff_LName': 'Lee'},
        {'Staff_ID': 2, 'Staff_FName': 'John', 'Staff_LName': 'Doe'},
        {'Staff_ID': 3, 'Staff_FName': 'Jane', 'Staff_LName': 'Smith'}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response
    # Run the function
    result = get_all_users_names()
    # Assertions
    expected_result = [
        {'Staff_ID': 1, 'Full_Name': 'Jaclyn Lee'},
        {'Staff_ID': 2, 'Full_Name': 'John Doe'},
        {'Staff_ID': 3, 'Full_Name': 'Jane Smith'}
    ]
    assert result == expected_result  # Check if the output matches the expected result
def test_get_all_users_names_no_data(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    # Mock response for no users found
    mock_response = MagicMock()
    mock_response.data = []  # No user data
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response
    # Run the function
    result = get_all_users_names()
    # Assertions
    assert result == []  # Should return an empty list if no users are found