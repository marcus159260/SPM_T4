import pytest
from unittest.mock import MagicMock

from controllers.user_controller import get_manager_details_data

def test_get_manager_details_data_success(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response for manager data
    mock_manager_response = MagicMock()
    mock_manager_response.data = [{
        'Staff_ID': 140008,
        'Staff_FName': 'Michael',
        'Staff_LName': 'Scott',
        'Dept': 'Sales',
        'Position': 'Regional Manager',
        'Country': 'USA'
    }]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_manager_response

    # Mock response for employees reporting to the manager
    mock_reporting_response = MagicMock()
    mock_reporting_response.data = [
        {'Dept': 'Sales', 'Position': 'Assistant Regional Manager', 'Country': 'USA'},
        {'Dept': 'Sales', 'Position': 'Sales Representative', 'Country': 'USA'},
        {'Dept': 'Sales', 'Position': 'Sales Representative', 'Country': 'Canada'}
    ]
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.side_effect = [
        mock_manager_response, mock_reporting_response
    ]

    # Run the function
    result = get_manager_details_data(manager_id=140008)

    # Expected result
    expected_result = {
        'Staff_ID': 140008,
        'Full_Name': 'Michael Scott',
        'Department': 'Sales',
        'Position': 'Regional Manager',
        'Country': 'USA',
        'In_Charge_Of': [
            ['Sales - Assistant Regional Manager - USA'],
            ['Sales - Sales Representative - USA'],
            ['Sales - Sales Representative - Canada']
        ]
    }

    # Assertions
    assert result['Staff_ID'] == expected_result['Staff_ID']
    assert result['Full_Name'] == expected_result['Full_Name']
    assert result['Department'] == expected_result['Department']
    assert result['Position'] == expected_result['Position']
    assert result['Country'] == expected_result['Country']
    assert sorted(result['In_Charge_Of']) == sorted(expected_result['In_Charge_Of'])

def test_get_manager_details_data_not_found(mocker):
    # Mock the Supabase client
    mock_supabase = mocker.patch('controllers.user_controller.supabase')

    # Mock response for manager data as not found
    mock_manager_response = MagicMock()
    mock_manager_response.data = None
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_manager_response

    # Run the function
    result = get_manager_details_data(manager_id=140008)

    # Assertions
    assert result is None
