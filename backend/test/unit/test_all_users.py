import pytest
from unittest.mock import MagicMock

from controllers.user_controller import get_all_users_data

def test_get_all_users_data(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for fetching all user data
    mock_response = MagicMock()
    mock_response.data = [
        {
            'Staff_ID': 140008,
            'Staff_FName': 'Jaclyn',
            'Staff_LName': 'Lee',
            'Role': 'Manager',
            'Position': 'Sales Manager',
            'Dept': 'Sales',
            'Reporting_Manager': 'Derek Tan'
        },
        {
            'Staff_ID': 140009,
            'Staff_FName': 'John',
            'Staff_LName': 'Doe',
            'Role': 'Employee',
            'Position': 'Sales Executive',
            'Dept': 'Sales',
            'Reporting_Manager': 'Jaclyn Lee'
        }
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response

    # Run the function
    result = get_all_users_data()

    # Assertions
    assert result == [
        {
            'Staff_ID': 140008,
            'Staff_FName': 'Jaclyn',
            'Staff_LName': 'Lee',
            'Role': 'Manager',
            'Position': 'Sales Manager',
            'Dept': 'Sales',
            'Reporting_Manager': 'Derek Tan'
        },
        {
            'Staff_ID': 140009,
            'Staff_FName': 'John',
            'Staff_LName': 'Doe',
            'Role': 'Employee',
            'Position': 'Sales Executive',
            'Dept': 'Sales',
            'Reporting_Manager': 'Jaclyn Lee'
        }
    ]


def test_get_no_usrs(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for fetching all user data
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response

    # Run the function
    result = get_all_users_data()

    # Assertions
    assert result == []