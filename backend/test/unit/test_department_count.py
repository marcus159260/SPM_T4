import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from controllers.user_controller import (
    get_department_wfh_wfo_counts,
    set_default_date_range,
    fetch_all_employees,
    build_departments_mapping,
    fetch_approved_wfh_requests,
    process_wfh_requests,
    calculate_department_counts
)

# Sample data for testing
sample_employees = [
    {'Dept': 'Engineering', 'Staff_ID': 1},
    {'Dept': 'Sales', 'Staff_ID': 2},
    {'Dept': 'Engineering', 'Staff_ID': 3},
]

sample_requests = [
    {'Staff_ID': 1, 'Start_Date': '2024-11-01', 'End_Date': '2024-11-01', 'Status': 'Approved'},
    {'Staff_ID': 2, 'Start_Date': '2024-11-03', 'End_Date': '2024-11-03', 'Status': 'Approved'},
    {'Staff_ID': 3, 'Start_Date': '2024-11-10', 'End_Date': '2024-11-10', 'Status': 'Approved'},
]

@pytest.fixture
def mock_supabase():
    with patch('controllers.user_controller.supabase') as mock_supabase:
        yield mock_supabase


def test_set_default_date_range_no_date():
    # Test without parameters (should return current week's Monday to Sunday)
    start_date, end_date = set_default_date_range(None, None)
    today = datetime.today()
    expected_start = today - timedelta(days=today.weekday())
    expected_end = expected_start + timedelta(days=6)

    assert start_date == expected_start
    assert end_date == expected_end


def test_set_default_date_range_date():

    # Test with provided dates
    start_date, end_date = set_default_date_range('2024-11-01', '2024-11-05')
    assert start_date == datetime(2024, 11, 1)
    assert end_date == datetime(2024, 11, 5)


def test_fetch_all_employees(mock_supabase):
    mock_response = MagicMock()
    mock_response.data = sample_employees
    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response

    employees = fetch_all_employees()

    assert employees == sample_employees
    mock_supabase.table.return_value.select.assert_called_once_with('Dept', 'Staff_ID')


def test_build_departments_mapping():
    departments = build_departments_mapping(sample_employees)
    assert departments == {
        'Engineering': {'total': 2, 'wfh': set()},
        'Sales': {'total': 1, 'wfh': set()}
    }


def test_fetch_approved_wfh_requests(mock_supabase):
    # Create a mock response with sample request data
    mock_response = MagicMock()
    mock_response.data = sample_requests

    # Mock the chain of method calls to return the mock response
    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    # Call the function
    requests = fetch_approved_wfh_requests()

    # Assertions to verify correct behavior
    assert requests == sample_requests
    mock_supabase.table.return_value.select.assert_called_once_with('Staff_ID', 'Start_Date', 'End_Date', 'Status')
    mock_supabase.table.return_value.select.return_value.eq.assert_called_once_with('Status', 'Approved')


def test_process_wfh_requests():
    # Mock data
    employees = sample_employees
    departments = build_departments_mapping(employees)
    requests = sample_requests

    # Set up the date range for the test
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 7)

    # Call the function to process requests
    process_wfh_requests(requests, employees, departments, start_date, end_date)

    # Check the departments mapping after processing
    assert departments['Engineering']['wfh'] == {1}  # Should contain Staff_ID 1
    assert departments['Sales']['wfh'] == {2}  # Should contain Staff_ID 2
    assert departments['Engineering']['total'] == 2  # Total employees in Engineering
    assert departments['Sales']['total'] == 1  # Total employees in Sales



def test_process_wfh_requests_more():
    departments = build_departments_mapping(sample_employees)
    start_date = datetime(2024, 11, 1)
    end_date = datetime(2024, 11, 10)

    process_wfh_requests(sample_requests, sample_employees, departments, start_date, end_date)

    assert departments['Engineering']['wfh'] == {1,3}
    assert departments['Sales']['wfh'] == {2}


def test_calculate_department_counts():
    # Mock input for departments
    departments = {
        'Engineering': {
            'total': 2,
            'wfh': {1}  # Staff_ID 1 is WFH
        },
        'Sales': {
            'total': 1,
            'wfh': {2}  # Staff_ID 2 is WFH
        }
    }

    # Call the function to test
    result = calculate_department_counts(departments)
    
    # Print the result for visibility (optional)
    print(result)

    # Expected output
    expected_result = [
        {'department': 'Engineering', 'wfh_count': 1, 'wfo_count': 1},  # 2 total, 1 WFH -> WFO 1
        {'department': 'Sales', 'wfh_count': 1, 'wfo_count': 0},        # 1 total, 1 WFH -> WFO 0
    ]

    # Assertions to verify the results
    assert result == expected_result



def test_get_department_wfh_wfo_counts(mock_supabase):
    # Mock the first call for fetching employees
    mock_employee_response = MagicMock()
    mock_employee_response.data = sample_employees
    
    # Mock the second call for fetching approved WFH requests
    mock_wfh_response = MagicMock()
    mock_wfh_response.data = sample_requests
    
    # Set up the side effect for the execute method
    mock_supabase.table.return_value.select.return_value.execute.side_effect = [
        mock_employee_response,  # First call returns employees
        mock_wfh_response         # Second call returns WFH requests
    ]
    
    # Call the function to test
    result = get_department_wfh_wfo_counts('2024-11-01', '2024-11-03')
    print(result)

    # Assertions to verify the results
    assert result == [
        {'department': 'Engineering', 'wfh_count': 1, 'wfo_count': 1},
        {'department': 'Sales', 'wfh_count': 1, 'wfo_count': 0},
    ]



# def test_end_to_end_flow():
#     # Define start and end dates for the test range
#     start_date = datetime.strptime('2024-11-01', '%Y-%m-%d')
#     end_date = datetime.strptime('2024-11-07', '%Y-%m-%d')

#     # Step 1: Build the departments mapping from sample employees
#     departments = build_departments_mapping(sample_employees)
#     print("Departments after initialization:")
#     print(departments)

#     # Step 2: Process WFH requests for the given date range
#     process_wfh_requests(sample_requests, sample_employees, departments, start_date, end_date)
#     print("Departments after processing WFH requests:")
#     print(departments)

#     # Step 3: Calculate department counts (WFO and WFH)
#     result = calculate_department_counts(departments)
#     print("Final result:")
#     print(result)

#     # Assert the expected outcome to validate the entire flow
#     expected_result = [
#         {'department': 'Engineering', 'wfh_count': 1, 'wfo_count': 1},
#         {'department': 'Sales', 'wfh_count': 1, 'wfo_count': 0},
#     ]
#     assert result == expected_result
