import pytest
from unittest.mock import MagicMock
from controllers.requests_controller import approve_withdrawal_wfh_request

@pytest.fixture
def mock_supabase(mocker):
    # Patch the `supabase` instance at the module level where it's used
    return mocker.patch('controllers.requests_controller.supabase')

def test_approve_withdrawal_wfh_request_success(mock_supabase):
    # Mock a successful update response
    mock_response = MagicMock()
    mock_response.data = [{'id': 1, 'Status': 'Withdrawn'}]  # Mocked data to simulate successful response
    mock_supabase.table().update().eq().execute.return_value = mock_response

    request_id = 1
    result = approve_withdrawal_wfh_request(request_id)
    
    assert result == ({'message': 'Request withdrawn successfully.'}, 200)
    mock_supabase.table().update().eq().execute.assert_called_once_with()  # Check if the function called execute

def test_approve_withdrawal_wfh_request_failure(mock_supabase):
    # Mock an exception being raised during update
    mock_supabase.table().update().eq().execute.side_effect = Exception("Database error")
    
    request_id = 1
    result = approve_withdrawal_wfh_request(request_id)

    assert result == {'error': 'Database error', 'status': 500}

def test_approve_withdrawal_wfh_request_no_request_found(mock_supabase):
    # Mock the select response to simulate no request found
    mock_response = MagicMock()
    mock_response.data = []  # No matching request found
    mock_supabase.table().select().eq().execute.return_value = mock_response
    
    request_id = 999  # ID that does not exist
    result = approve_withdrawal_wfh_request(request_id)

    assert result == ({'error': 'No request found for the given ID'}, 500)  


def test_approve_wfh_withdrawal_request_update_failure(mock_supabase):
    # Mock a successful fetch response but simulate an update failure
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Status': 'Pending'}]  # Assuming this is a pending request
    mock_supabase.table().select().eq().execute.return_value = mock_response

    # Mock an exception when trying to update the request
    mock_supabase.table().update().eq().execute.side_effect = Exception("Update error")

    request_id = 1
    reason = "Request was not valid"
    result = approve_withdrawal_wfh_request(request_id)

    assert result == ({'error': 'Update error', 'status': 500})
