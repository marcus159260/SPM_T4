import pytest
from unittest.mock import MagicMock
from controllers.requests_controller import reject_wfh_withdrawal_request

@pytest.fixture
def mock_supabase(mocker):
    # Patch the `supabase` instance at the module level where it's used
    return mocker.patch('controllers.requests_controller.supabase')

def test_reject_wfh_withdrawal_request_success(mock_supabase):
    # Mock a successful response for fetching the request
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Status': 'Pending'}]  # Assuming this is a pending request
    mock_supabase.table().select().eq().execute.return_value = mock_response

    # Mock a successful update response
    update_response = MagicMock()
    update_response.data = []
    mock_supabase.table().update().eq().execute.return_value = update_response

    request_id = 1
    reason = "Request was not valid"
    result = reject_wfh_withdrawal_request(request_id, reason)

    assert result == ({'message': 'Request rejected successfully.'}, 200)

def test_reject_wfh_withdrawal_request_empty_reason(mock_supabase):
    request_id = 1
    reason = ""
    result = reject_wfh_withdrawal_request(request_id, reason)

    assert result == ({'message': 'Reason cannot be empty.'}, 500)

def test_reject_wfh_withdrawal_request_exception_handling(mock_supabase):
    # Mock an exception when fetching the request
    mock_supabase.table().select().eq().execute.side_effect = Exception("Some error")

    request_id = 1
    reason = "Request was not valid"
    result = reject_wfh_withdrawal_request(request_id, reason)

    assert result == ({'error': 'Some error', 'status': 500})

def test_reject_wfh_withdrawal_request_no_request_found(mock_supabase):
    # Mock a response where no request is found
    mock_response = MagicMock()
    mock_response.data = []  # No request found for the given ID
    mock_supabase.table().select().eq().execute.return_value = mock_response

    request_id = 1
    reason = "Request was not valid"
    result = reject_wfh_withdrawal_request(request_id, reason)

    # Ensure the expected output matches what the function actually returns
    expected_output = {'error': 'No request found for the given ID'}, 500
    assert result == expected_output


def test_reject_wfh_withdrawal_request_update_failure(mock_supabase):
    # Mock a successful fetch response but simulate an update failure
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Status': 'Pending'}]  # Assuming this is a pending request
    mock_supabase.table().select().eq().execute.return_value = mock_response

    # Mock an exception when trying to update the request
    mock_supabase.table().update().eq().execute.side_effect = Exception("Update error")

    request_id = 1
    reason = "Request was not valid"
    result = reject_wfh_withdrawal_request(request_id, reason)

    assert result == ({'error': 'Update error', 'status': 500})
