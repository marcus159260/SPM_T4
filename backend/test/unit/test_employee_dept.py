import pytest
from unittest.mock import MagicMock
from controllers.user_controller import get_employees_by_dept_data
def test_get_employees_by_dept_data(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for employees in Engineering department with Call Centre position
    mock_employee_response = MagicMock()
    mock_employee_response.data = [
        {'Staff_ID': 1, 'Dept': 'Engineering', 'Position': 'Call Centre', 'Reporting_Manager': 101},
        {'Staff_ID': 2, 'Dept': 'Engineering', 'Position': 'Call Centre', 'Reporting_Manager': 102}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_employee_response
    # Mock response for managers based on Reporting_Manager IDs
    mock_managers_response = MagicMock()
    mock_managers_response.data = [
        {'Staff_ID': 101, 'Staff_FName': 'John', 'Staff_LName': 'Doe'},
        {'Staff_ID': 102, 'Staff_FName': 'Jane', 'Staff_LName': 'Smith'}
    ]
    mock_supabase.table.return_value.select.return_value.in_.return_value.execute.return_value = mock_managers_response
    # Run the function
    result = get_employees_by_dept_data()
    # Expected result
    expected_result = [
        {'Staff_ID': 1, 'Dept': 'Engineering', 'Position': 'Call Centre', 'Reporting_Manager': 101, 'Manager_Name': 'John Doe'},
        {'Staff_ID': 2, 'Dept': 'Engineering', 'Position': 'Call Centre', 'Reporting_Manager': 102, 'Manager_Name': 'Jane Smith'}
    ]
    # Assertions, check the result contains the expected entries with Manager_Name added
    assert len(result) == len(expected_result)
    assert all(employee in result for employee in expected_result)
def test_get_employees_by_dept_empty(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')
    
    # Mock response for employees in Engineering department with Call Centre position
    mock_employee_response = MagicMock()
    mock_employee_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.execute.return_value = mock_employee_response
    result = get_employees_by_dept_data()
    # Assertions, check the result contains the expected entries with Manager_Name added
    assert len(result) == 0