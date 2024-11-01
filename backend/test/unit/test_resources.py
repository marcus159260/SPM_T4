import pytest
from unittest.mock import MagicMock
from controllers.user_controller import get_resources
def test_get_resources_with_tree_building(mocker):
    # Mock the Supabase client to simulate database response
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    mock_response = mocker.MagicMock()
    mock_response.data = [
        {'Dept': 'Engineering', 'Position': 'Developer', 'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith', 'Reporting_Manager': 101},
        {'Dept': 'Sales', 'Position': 'Sales Manager', 'Staff_ID': 101, 'Staff_FName': 'John', 'Staff_LName': 'Doe', 'Reporting_Manager': None}
    ]
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response
    # Optionally, if `group_employees_by_department` and `build_department_hierarchy` are complex,
    # you could mock them as well if you only need to validate the higher-level flow.
    
    # Define expected output for build_resource_tree
    expected_output = [
        {
            'name': 'Engineering',
            'id': 'D_Engineering',
            'expanded': True,
            'children': []
        },
        {
            'name': 'Sales',
            'id': 'D_Sales',
            'expanded': True,
            'children': []
        }
    ]
    # Run the function
    result = get_resources()
    # Assertions
    assert result == expected_output
    mock_supabase.table.return_value.select.assert_called_once_with(
        'Dept', 'Position', 'Staff_ID', 'Staff_FName', 'Staff_LName', 'Reporting_Manager'
    )
def test_get_resources_exception_handling_with_output(capsys, mocker):
    # Mock the Supabase client to simulate an exception during data fetching
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    mock_supabase.table.return_value.select.return_value.execute.side_effect = Exception("Database error")
    # Run the function
    result = get_resources()
    # Assertions
    assert result is None  # Should return None when an exception occurs
    # Capture print output
    captured = capsys.readouterr()
    assert "Error fetching employee data: Database error" in captured.out