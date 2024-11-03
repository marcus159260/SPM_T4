import pytest
from unittest.mock import MagicMock

from controllers.auth_controller import authenticate_user

def test_authenticate_user_success(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.auth_controller.supabase')

    # Mock response for a successful authentication
    mock_response = MagicMock()
    mock_response.data = {
        'Staff_ID': 140008,  # Correct key: Staff_ID with uppercase
        'Role': 3,
        'Position': 'Sales Manager',
        'Dept': 'Sales',
        'Staff_FName': 'Jaclyn',
        'Staff_LName': 'Lee',
        'Reporting_Manager': 140001
    }
    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    # Run the function
    result = authenticate_user(staff_id=140008)

    # Assertions
    assert result == {
        'staff_id': 140008,
        'role': 3,
        'position': 'Sales Manager',
        'department': 'Sales',
        'staff_fname': 'Jaclyn',
        'staff_lname': 'Lee',
        'reporting_manager': 140001
    }

def test_authenticate_user_not_found(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.auth_controller.supabase')

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.side_effect = Exception("Staff not found")

    # Run the function
    result = authenticate_user(staff_id=140008)

    # Assertions
    assert result is None  # Should return None if no user is found

def test_authenticate_user_exception(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.auth_controller.supabase')

    # Mock response to raise an exception for the database query
    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.side_effect = Exception("Database error")

    # Run the function
    result = authenticate_user(staff_id=140008)

    # Assertions
    assert result is None  # Should return None if an exception occurs
