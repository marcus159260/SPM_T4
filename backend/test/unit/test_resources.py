import pytest
from unittest.mock import MagicMock

from controllers.user_controller import get_resources, build_resource_tree

def test_get_resources_with_tree_building(mocker):
    # Mock the Supabase client to simulate database response
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    mock_response = mocker.MagicMock()
    mock_response.data = [
        {'Dept': 'Engineering', 'Position': 'Developer', 'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith', 'Reporting_Manager': 101, 'Role':3},
        {'Dept': 'Sales', 'Position': 'Sales Manager', 'Staff_ID': 101, 'Staff_FName': 'John', 'Staff_LName': 'Doe', 'Reporting_Manager': None,"Role":1}
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
        'Dept', 'Position', 'Staff_ID', 'Staff_FName', 'Staff_LName', 'Reporting_Manager', 'Role'
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


def test_build_resource_tree(mocker):
    # Sample input data
    data = [
        {'Dept': 'Engineering', 'Position': 'Developer', 'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith', 'Reporting_Manager': 2, },
        {'Dept': 'Sales', 'Position': 'Sales Manager', 'Staff_ID': 2, 'Staff_FName': 'John', 'Staff_LName': 'Doe', 'Reporting_Manager': 3,  }
    ]

    # Mock the group_employees_by_department function to return grouped data
    mock_group_employees = mocker.patch('controllers.user_controller.group_employees_by_department')
    mock_group_employees.return_value = {
        'Engineering': [data[0]],
        'Sales': [data[1]]
    }

    # Mock the build_department_hierarchy function to return simple structures for the employees
    mock_build_hierarchy = mocker.patch('controllers.user_controller.build_department_hierarchy')
    mock_build_hierarchy.side_effect = lambda employees: [{'name': f"{e['Staff_FName']} {e['Staff_LName']}", 'id': f"S_{e['Staff_ID']}"} for e in employees]

    # Expected output
    expected_output = [
        {
            'name': 'Engineering',
            'id': 'D_Engineering',
            'expanded': True,
            'children': [{'name': 'Alice Smith', 'id': 'S_1'}]
        },
        {
            'name': 'Sales',
            'id': 'D_Sales',
            'expanded': True,
            'children': [{'name': 'John Doe', 'id': 'S_2'}]
        }
    ]

    # Run the function
    result = build_resource_tree(data)

    # Assertions
    assert result == expected_output
    mock_group_employees.assert_called_once_with(data)
    mock_build_hierarchy.assert_any_call([data[0]])
    mock_build_hierarchy.assert_any_call([data[1]])