import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock
from controllers.user_controller import (
    get_department_wfh_wfo_counts,
    set_default_date_range,
    fetch_all_employees,
    build_departments_mapping,
    fetch_approved_wfh_requests,
    process_wfh_requests,
    calculate_department_counts
)

@pytest.fixture
def sample_employees():
    return [
        {'Dept': 'Engineering', 'Staff_ID': 1},
        {'Dept': 'Sales', 'Staff_ID': 2},
        {'Dept': 'Engineering', 'Staff_ID': 3},
    ]

@pytest.fixture
def sample_requests():
    return [
        {'Staff_ID': 1, 'Start_Date': '2024-11-01', 'End_Date': '2024-11-01', 'Status': 'Approved'},
        {'Staff_ID': 2, 'Start_Date': '2024-11-03', 'End_Date': '2024-11-03', 'Status': 'Approved'},
        {'Staff_ID': 3, 'Start_Date': '2024-11-10', 'End_Date': '2024-11-10', 'Status': 'Approved'},
    ]

@pytest.fixture
def mock_supabase(mocker):
    # Create a mock response for the Supabase client
    mock_client = MagicMock()
    mock_client.table.return_value.select.return_value.eq.return_value.execute.return_value.data = []
    mocker.patch('controllers.user_controller.supabase', mock_client)
    return mock_client

def test_set_default_date_range_no_date():
    start_date, end_date = set_default_date_range(None, None)
    today = datetime.today()
    expected_start = today - timedelta(days=today.weekday())
    expected_end = expected_start + timedelta(days=6)

    assert start_date.date() == expected_start.date()
    assert end_date.date() == expected_end.date()

def test_set_default_date_range_date():
    start_date, end_date = set_default_date_range('2024-11-01', '2024-11-05')
    assert start_date == datetime(2024, 11, 1)
    assert end_date == datetime(2024, 11, 5)

def test_fetch_all_employees(mocker, mock_supabase, sample_employees):
    # Set the mock response for fetch_all_employees
    mock_supabase.table.return_value.select.return_value.execute.return_value.data = sample_employees

    employees = fetch_all_employees()

    assert employees == sample_employees
    mock_supabase.table.return_value.select.assert_called_once_with('Dept', 'Staff_ID')

def test_build_departments_mapping(sample_employees):
    departments = build_departments_mapping(sample_employees)
    assert departments == {
        'Engineering': {'total': 2, 'wfh': set()},
        'Sales': {'total': 1, 'wfh': set()}
    }

def test_fetch_approved_wfh_requests(mocker, mock_supabase, sample_requests):
    # Set the mock response for fetch_approved_wfh_requests
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value.data = sample_requests

    # Call the function under test
    requests = fetch_approved_wfh_requests()

    # Assert that the result is as expected
    assert requests == sample_requests

    # Check that the necessary calls were made to the mocked client
    mock_supabase.table.assert_called_once_with('request')
    mock_supabase.table.return_value.select.assert_called_once_with('Staff_ID', 'Start_Date', 'End_Date', 'Status')
    mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('Status', 'Approved')
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.assert_called_once()


def test_process_wfh_requests(sample_employees, sample_requests):
    departments = build_departments_mapping(sample_employees)
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 7)

    process_wfh_requests(sample_requests, sample_employees, departments, start_date, end_date)

    assert departments['Engineering']['wfh'] == {1}
    assert departments['Sales']['wfh'] == {2}
    assert departments['Engineering']['total'] == 2
    assert departments['Sales']['total'] == 1

def test_process_wfh_requests_more(sample_employees, sample_requests):
    departments = build_departments_mapping(sample_employees)
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 10)

    process_wfh_requests(sample_requests, sample_employees, departments, start_date, end_date)

    assert departments['Engineering']['wfh'] == {1, 3}
    assert departments['Sales']['wfh'] == {2}

def test_calculate_department_counts():
    departments = {
        'Engineering': {
            'total': 2,
            'wfh': {1}
        },
        'Sales': {
            'total': 1,
            'wfh': {2}
        }
    }

    result = calculate_department_counts(departments)
    
    expected_result = [
        {'department': 'Engineering', 'wfh_count': 1, 'wfo_count': 1},
        {'department': 'Sales', 'wfh_count': 1, 'wfo_count': 0},
    ]

    assert result == expected_result

def test_get_department_wfh_wfo_counts(mocker, sample_employees, sample_requests):
    # Arrange: Mock the functions that the function under test relies on
    mock_set_default_date_range = mocker.patch('controllers.user_controller.set_default_date_range', return_value=('2024-11-01', '2024-11-10'))
    mock_fetch_all_employees = mocker.patch('controllers.user_controller.fetch_all_employees', return_value=sample_employees)
    mock_fetch_approved_wfh_requests = mocker.patch('controllers.user_controller.fetch_approved_wfh_requests', return_value=sample_requests)
    
    departments = {
        'Engineering': {'WFH_Count': 0, 'WFO_Count': 0},
        'Sales': {'WFH_Count': 0, 'WFO_Count': 0},
    }
    mock_build_departments_mapping = mocker.patch('controllers.user_controller.build_departments_mapping', return_value=departments)
    mock_process_wfh_requests = mocker.patch('controllers.user_controller.process_wfh_requests')
    mock_calculate_department_counts = mocker.patch(
        'controllers.user_controller.calculate_department_counts',
        return_value={'Engineering': {'WFH_Count': 2, 'WFO_Count': 0}, 'Sales': {'WFH_Count': 1, 'WFO_Count': 0}}
    )

    # Act: Call the function
    result = get_department_wfh_wfo_counts()

    # Assert: Verify the result and function calls
    assert result == {'Engineering': {'WFH_Count': 2, 'WFO_Count': 0}, 'Sales': {'WFH_Count': 1, 'WFO_Count': 0}}
    mock_set_default_date_range.assert_called_once()
    mock_fetch_all_employees.assert_called_once()
    mock_fetch_approved_wfh_requests.assert_called_once()
    mock_build_departments_mapping.assert_called_once_with(sample_employees)
    mock_process_wfh_requests.assert_called_once_with(
        sample_requests,
        sample_employees,
        departments,
        '2024-11-01',
        '2024-11-10'
    )
    mock_calculate_department_counts.assert_called_once_with(departments)
