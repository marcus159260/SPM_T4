import pytest
from unittest.mock import MagicMock

from controllers.user_controller import get_employees_by_reporting_manager

def test_get_employees_by_reporting_manager_success(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response for employees reporting to the manager
    mock_team_response = MagicMock()
    mock_team_response.data = [
        {'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith'},
        {'Staff_ID': 2, 'Staff_FName': 'Bob', 'Staff_LName': 'Johnson'}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_team_response

    # Mock response for the reporting manager
    mock_manager_response = MagicMock()
    mock_manager_response.data = [
        {'Staff_ID': 140894, 'Staff_FName': 'Charlie', 'Staff_LName': 'Brown'}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_manager_response

    # Run the function
    result = get_employees_by_reporting_manager(reporting_manager_id=140894)

    # Assertions
    expected_result = [
        {'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith'},
        {'Staff_ID': 2, 'Staff_FName': 'Bob', 'Staff_LName': 'Johnson'},
        {'Staff_ID': 140894, 'Staff_FName': 'Charlie', 'Staff_LName': 'Brown'}
    ]
    
    assert result == expected_result


def test_get_employees_by_reporting_manager_no_team(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response for no employees reporting to the manager
    mock_team_response = MagicMock()
    mock_team_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_team_response

    # Mock response for the reporting manager
    mock_manager_response = MagicMock()
    mock_manager_response.data = [
        {'Staff_ID': 140894, 'Staff_FName': 'Charlie', 'Staff_LName': 'Brown'}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_manager_response

    # Run the function
    result = get_employees_by_reporting_manager(reporting_manager_id=140894)

    # Assertions
    expected_result = [
        {'Staff_ID': 140894, 'Staff_FName': 'Charlie', 'Staff_LName': 'Brown'}
    ]

    assert result == expected_result