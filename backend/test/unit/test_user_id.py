import pytest
from unittest.mock import MagicMock

from controllers.user_controller import get_user_data_by_id

def test_get_user_data_by_id_found(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for a successful user lookup
    mock_response = MagicMock()
    mock_response.data = [{
        'Staff_ID': 140008,
        'Staff_FName': 'Jaclyn',
        'Staff_LName': 'Lee',
        'Role': 'Manager',
        'Position': 'Sales Manager',
        'Dept': 'Sales',
        'Reporting_Manager': 'Derek Tan'
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = get_user_data_by_id(140008)

    # Assertions for a successful retrieval
    assert result == {
        'Staff_ID': 140008,
        'Staff_FName': 'Jaclyn',
        'Staff_LName': 'Lee',
        'Role': 'Manager',
        'Position': 'Sales Manager',
        'Dept': 'Sales',
        'Reporting_Manager': 'Derek Tan'
    }


def test_get_user_data_by_id_not_found(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for an unsuccessful user lookup
    mock_response = MagicMock()
    mock_response.data = None  # Simulate no data found
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Run the function
    result = get_user_data_by_id(140008)

    # Assertions for no user found
    assert result is None
