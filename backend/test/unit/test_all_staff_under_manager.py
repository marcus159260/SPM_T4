import pytest
from unittest.mock import MagicMock
from controllers.user_controller import get_all_employees_below_reporting_manager

# check structure of the result
def test_get_all_employees_below_reporting_manager(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response for employees reporting to the manager (ID 5)
    mock_team_response = MagicMock()
    mock_team_response.data = [
        {'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith', 'Reporting_Manager': 5, 'Dept': 'Engineering', 'Position': 'Manager', 'Role': 3},
        {'Staff_ID': 2, 'Staff_FName': 'Bob', 'Staff_LName': 'Johnson', 'Reporting_Manager': 5, 'Dept': 'Sales', 'Position': 'Manager', 'Role': 3}    
        ]

    # Mock response for subordinates of Alice (Reporting_Manager=1)
    mock_subordinate_response = MagicMock()
    mock_subordinate_response.data = [
        {'Staff_ID': 3, 'Staff_FName': 'Charles', 'Staff_LName': 'Tan', 'Reporting_Manager': 1, 'Dept': 'Engineering', 'Position': 'Junior Engineer', 'Role': 2}
    ]

    # Mock response for employees with no subordinates (i.e., base case for recursion)
    empty_response = MagicMock()
    empty_response.data = []

    # Set up the side_effect to simulate recursive behavior
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_team_response,  # Initial call for reporting_manager_id=5 (Alice, Bob)
        mock_subordinate_response,  # Recursive call for Staff_ID=1 (Alice Smith)
        empty_response,  # Recursive call for Staff_ID=2 (Bob Johnson) - no subordinates
        empty_response  # Recursive call for Staff_ID=3 (Charles Tan) - no subordinates
    ]

    # Run the function
    result = get_all_employees_below_reporting_manager(reporting_manager_id=5)

    # Debugging print statement to inspect the result
    print(f"Result: {result}")

    # Assertions
    expected_result = [
        {
            'Staff_ID': 1,
            'Staff_FName': 'Alice',
            'Staff_LName': 'Smith',
            'Reporting_Manager': 5,
            'Dept': 'Engineering',
            'Position': 'Manager',
            'Role': 3,
            'name': 'Alice Smith\nEngineering (Manager)',
            'children': [
                {
                    'Staff_ID': 3,
                    'Staff_FName': 'Charles',
                    'Staff_LName': 'Tan',
                    'Reporting_Manager': 1,
                    'Dept': 'Engineering',
                    'Position': 'Junior Engineer',
                    'Role': 2,
                    'name': 'Charles Tan\nEngineering (Junior Engineer)',
                    'children': [],
                    'id': 'E_3'
                }
            ],
            'id': 'E_1'
        },
        {
            'Staff_ID': 2,
            'Staff_FName': 'Bob',
            'Staff_LName': 'Johnson',
            'Reporting_Manager': 5,
            'Dept': 'Sales',
            'Position': 'Manager',
            'Role': 3,
            'name': 'Bob Johnson\nSales (Manager)',
            'children': [],
            'id': 'E_2'
        }
    ]

    # Check if the lengths match
    assert len(result) == len(expected_result), f"Expected {len(expected_result)} but got {len(result)}"
    
    # Assertions to check if the structure matches the expected result
    assert result == expected_result



def test_get_all_employees_below_reporting_manager_empty(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response with no employees under the reporting manager
    mock_team_response = MagicMock()
    mock_team_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_team_response

    # Run the function with a reporting manager ID that has no team members
    result = get_all_employees_below_reporting_manager(100)

    # Assertions
    assert result == []