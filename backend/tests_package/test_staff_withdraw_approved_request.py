import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from freezegun import freeze_time

from controllers.requests_controller import withdraw_request_controller

def test_invalid_input():
    result, status_code = withdraw_request_controller(None, "Reason", 150076)
    assert status_code == 400
    assert result['error'] == 'Invalid input'

    result, status_code = withdraw_request_controller(1, None, 150076)
    assert status_code == 400
    assert result['error'] == 'Invalid input'

@freeze_time("2024-10-20")
def test_request_not_found(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = None

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    result, status_code = withdraw_request_controller(99999, "Reason", 150076)
    print(f"test_request_not_found: result={result}, status_code={status_code}")
    assert status_code == 404
    assert result['error'] == 'Request not found'

def test_unauthorized_user(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = {
        'Request_ID': 1,
        'Staff_ID': 999999,  # Different Staff_ID to simulate unauthorized access
        'Start_Date': '2024-10-15',
        'End_Date': '2024-10-16',
        'Status': 'Approved'
    }

    mock_supabase.table.return_value.select.return_value.eq.return_value.single.return_value.execute.return_value = mock_response
    
    result, status_code = withdraw_request_controller(1, "Reason", 999999)
    print(f"test_unauthorized_user: result={result}, status_code={status_code}")
    assert status_code == 403
    assert result['error'] == 'Unauthorized'

@freeze_time("2024-10-20")
def test_withdraw_outside_allowed_timeframe(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = {
        'Request_ID': 1,
        'Staff_ID': 150076,
        'Start_Date': '2024-09-20',
        'End_Date': '2024-09-30',
        'Status': 'Approved'
    }

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    result, status_code = withdraw_request_controller(1, "Reason", 150076)
    print(f"test_withdraw_outside_allowed_timeframe: result={result}, status_code={status_code}")
    assert status_code == 400
    assert result['error'] == 'Cannot withdraw request outside the allowed time frame'

@freeze_time("2024-10-20")
def test_successful_withdrawal(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = {
        'Request_ID': 1,
        'Staff_ID': 150076,
        'Start_Date': '2024-10-15',
        'End_Date': '2024-10-16',
        'Status': 'Approved'
    }

    mock_response_update = MagicMock()
    mock_response_update.data = None

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response_update

    result, status_code = withdraw_request_controller(1, "Valid reason", 150076)
    print(f"test_successful_withdrawal: result={result}, status_code={status_code}")
    assert status_code == 200
    assert result['message'] == 'Request withdrawn successfully'

@freeze_time("2024-10-01")  # Assuming start_date is 2024-10-15
def test_withdrawal_on_earliest_allowed_date(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = {
        'Request_ID': 1,
        'Staff_ID': 150076,
        'Start_Date': '2024-10-15',  # Start date
        'End_Date': '2024-10-16',    # End date
        'Status': 'Approved'
    }

    mock_response_update = MagicMock()
    mock_response_update.data = None

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response_update

    result, status_code = withdraw_request_controller(1, "Boundary test reason", 150076)
    print(f"test_withdrawal_on_earliest_allowed_date: result={result}, status_code={status_code}")
    assert status_code == 200
    assert result['message'] == 'Request withdrawn successfully'

@freeze_time("2024-10-30")  # Assuming end_date is 2024-10-16
def test_withdrawal_on_latest_allowed_date(mocker):
    # Patch the correct supabase object
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = {
        'Request_ID': 2,
        'Staff_ID': 150076,
        'Start_Date': '2024-10-15',  # Start date
        'End_Date': '2024-10-16',    # End date
        'Status': 'Approved'
    }

    mock_response_update = MagicMock()
    mock_response_update.data = None

    mock_supabase.table.return_value.select.return_value.eq.return_value.maybe_single.return_value.execute.return_value = mock_response

    mock_supabase.table.return_value.update.return_value.eq.return_value.execute.return_value = mock_response_update

    result, status_code = withdraw_request_controller(2, "Boundary test reason", 150076)
    print(f"test_withdrawal_on_latest_allowed_date: result={result}, status_code={status_code}")
    assert status_code == 200
    assert result['message'] == 'Request withdrawn successfully'