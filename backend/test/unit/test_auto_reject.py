import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from controllers.requests_controller import auto_reject_pending_requests 

@pytest.fixture
def mock_supabase(mocker):
    return mocker.patch('controllers.requests_controller.supabase')

def test_auto_reject_pending_requests_with_rejections(mock_supabase):
    # Mock current date
    current_date = datetime.now().date()
    
    # Mock response with pending requests older than 2 months
    mock_response = MagicMock()
    mock_response.data = [
        {'Request_ID': 1, 'Start_Date': (current_date - relativedelta(months=3)).strftime("%Y-%m-%d"), 'Status': 'Pending', 'Approver_ID': '123'},
        {'Request_ID': 2, 'Start_Date': (current_date - relativedelta(months=1)).strftime("%Y-%m-%d"), 'Status': 'Pending', 'Approver_ID': '123'},
    ]
    mock_supabase.table().select().eq().eq().execute.return_value = mock_response
    
    rejected_count = auto_reject_pending_requests('123')

    # Verify that one request was rejected
    assert rejected_count == 1
    mock_supabase.table().update.assert_called_once_with({'Status': 'Rejected', 'Rejection_Reason': 'Auto-rejected after 2 months'})

def test_auto_reject_pending_requests_no_requests(mock_supabase):
    # Mock response with no pending requests
    mock_response = MagicMock()
    mock_response.data = []
    mock_supabase.table().select().eq().eq().execute.return_value = mock_response
    
    rejected_count = auto_reject_pending_requests('123')

    # Verify that no requests were rejected
    assert rejected_count == 0

def test_auto_reject_pending_requests_no_old_requests(mock_supabase):
    # Mock current date
    current_date = datetime.now().date()
    
    # Mock response with all requests younger than 2 months
    mock_response = MagicMock()
    mock_response.data = [
        {'Request_ID': 1, 'Start_Date': (current_date - relativedelta(months=1)).strftime("%Y-%m-%d"), 'Status': 'Pending', 'Approver_ID': '123'},
        {'Request_ID': 2, 'Start_Date': (current_date - timedelta(days=10)).strftime("%Y-%m-%d"), 'Status': 'Pending', 'Approver_ID': '123'},
    ]
    mock_supabase.table().select().eq().eq().execute.return_value = mock_response
    
    rejected_count = auto_reject_pending_requests('123')

    # Verify that no requests were rejected
    assert rejected_count == 0

def test_auto_reject_pending_requests_exception_handling(mock_supabase):
    # Simulate an exception being raised
    mock_supabase.table().select().eq().eq().execute.side_effect = Exception("Database error")

    rejected_count = auto_reject_pending_requests('123')

    # Verify that the function returns 0 on exception
    assert rejected_count == 0