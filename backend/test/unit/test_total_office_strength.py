import pytest
from unittest.mock import MagicMock
from controllers.requests_controller import get_total_office_strength

def test_get_total_office_strength(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock the response from the database
    mock_response = MagicMock()
    mock_response.data = [
        {'Employee_ID': 1, 'Name': 'John Doe', 'Reporting_Manager': 1},
        {'Employee_ID': 2, 'Name': 'Jane Smith', 'Reporting_Manager': 1}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Call the function with a valid managerId
    total_strength = get_total_office_strength(managerId=1)

    # Assertions
    assert total_strength == 2  # Expecting 2 employees under managerId 1
    mock_supabase.table.return_value.select.assert_called_once_with("*")
    mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('Reporting_Manager', 1)


def test_get_total_office_strength_no_employees(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock the response to have no employees
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Call the function with a valid managerId
    total_strength = get_total_office_strength(managerId=1)

    # Assertions
    assert total_strength == 0  # Expecting 0 employees under managerId 1


def test_get_total_office_strength_with_exception(mocker, capfd):
    # Mock the Supabase client to raise an exception
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = Exception("Database error")

    # Call the function, which should now raise the mocked exception
    total_strength = get_total_office_strength(managerId=1)

    # Capture the output
    captured = capfd.readouterr()

    # Assertions
    assert total_strength == 0  # Expecting 0 because of the exception
    assert "Error retrieving total office strength: Database error" in captured.out  # Check the printed output
