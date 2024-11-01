
import pytest
from unittest.mock import MagicMock

from controllers.requests_controller import log_activity

def test_log_activity_success(mocker):
    # Mock Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response for the RPC call
    mock_response = MagicMock()
    mock_response.data = [{'status': 'success'}]  # Simulate a successful logging response
    mock_supabase.rpc.return_value.execute.return_value = mock_response

    # Parameters for the log_activity function
    request_id = 1
    old_status = 'Pending'
    new_status = 'Approved'
    changed_by = 140008
    change_message = 'Request approved by manager'
    reason = 'All requirements met'

    # Run the function
    result = log_activity(request_id, old_status, new_status, changed_by, change_message, reason)

    # Assertions
    assert result == mock_response  # Ensure the result is as expected
    mock_supabase.rpc.assert_called_once_with('log_activity', {
        'p_request_id': request_id,
        'p_old_status': old_status,
        'p_new_status': new_status,
        'p_changed_by': changed_by,
        'p_change_message': change_message,
        'p_reason': reason
    })


def test_log_activity_failure(mocker):
    # Mock Supabase client
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')

    # Mock response to raise an exception for the RPC call
    mock_supabase.rpc.return_value.execute.side_effect = Exception("Logging error")

    # Parameters for the log_activity function
    request_id = 1
    old_status = 'Pending'
    new_status = 'Approved'
    changed_by = 140008
    change_message = 'Request approved by manager'
    reason = 'All requirements met'

    # Run the function and check for exception
    with pytest.raises(Exception, match="Logging error"):
        log_activity(request_id, old_status, new_status, changed_by, change_message, reason)
