import pytest
from unittest.mock import MagicMock

from controllers.requests_controller import get_staff_requests_data, get_staff_events_data, get_all_events_data, build_events


def test_get_staff_requests_data_found(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    result = get_staff_requests_data(140008)
    assert result == mock_response.data


def test_get_staff_requests_data_not_found(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = None

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    result = get_staff_requests_data(140008)
    assert result is None


def test_get_staff_events_data_success(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.eq.return_value.execute.return_value = mock_response

    mock_build_events = mocker.patch('controllers.requests_controller.build_events')
    mock_build_events.return_value = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY'}]

    result = get_staff_events_data(140008)
    assert result == mock_build_events.return_value


def test_get_staff_events_data_exception(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_supabase.table.side_effect = Exception("Database Error")

    result = get_staff_events_data(140008)
    assert result is None


def test_get_all_events_data_success(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_response = MagicMock()
    mock_response.data = [{'Request_ID': 1, 'Staff_ID': 140008, 'Status': 'Pending','Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY','Reason': 'Sick'}]

    mock_supabase.table.return_value.select.return_value.execute.return_value = mock_response

    mock_build_events = mocker.patch('controllers.requests_controller.build_events')
    mock_build_events.return_value = [{'id': '1_2024-10-01', 'start': '2024-10-01T09:00:00', 'end': '2024-10-01T18:00:00'}]

    result = get_all_events_data()
    assert result == mock_build_events.return_value


def test_get_all_events_data_exception(mocker):
    mock_supabase = mocker.patch('controllers.requests_controller.supabase')
    mock_supabase.table.side_effect = Exception("Database Error")

    result = get_all_events_data()
    assert result is None


def test_build_events_len():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY', 'Status': 'Approved'},
        {'Request_ID': 2, 'Staff_ID': 150077, 'Start_Date': '2024-10-03', 'End_Date': '2024-10-03', 'Time': 'AM', 'Status': 'Approved'},
    ]

    result = build_events(sample_data)

    assert len(result) == 2


def test_build_events_approved():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY', 'Status': 'Approved'},
        {'Request_ID': 2, 'Staff_ID': 150077, 'Start_Date': '2024-10-03', 'End_Date': '2024-10-03', 'Time': 'AM', 'Status': 'Pending'},
    ]

    result = build_events(sample_data)

    assert len(result) == 1


def test_build_events_unknown_time_slot(capfd):
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'MORNING', 'Status': 'Approved'},
        {'Request_ID': 2, 'Staff_ID': 150077, 'Start_Date': '2024-10-02', 'End_Date': '2024-10-02', 'Time': 'FULL DAY', 'Status': 'Approved'},
    ]

    result = build_events(sample_data)

    # Capture the output
    captured = capfd.readouterr()
    
    # Check if the specific message for unknown time slot was printed
    assert "Unknown time slot: MORNING" in captured.out
    # Ensure only the valid event was created
    assert len(result) == 1
    assert result[0]['id'].startswith("2")


def test_build_events_am():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'AM', 'Status': 'Approved'}]

    result = build_events(sample_data)

    assert result[0]['start'] == '2024-10-01T09:00:00'
    assert result[0]['end'] == '2024-10-01T13:00:00'


def test_build_events_pm():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'PM', 'Status': 'Approved'}]

    result = build_events(sample_data)

    assert result[0]['start'] == '2024-10-01T14:00:00'
    assert result[0]['end'] == '2024-10-01T18:00:00'


def test_build_events_fullday():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY', 'Status': 'Approved'}]

    result = build_events(sample_data)

    assert result[0]['start'] == '2024-10-01T09:00:00'
    assert result[0]['end'] == '2024-10-01T18:00:00'


def test_build_events_eventid():
    sample_data = [
        {'Request_ID': 1, 'Staff_ID': 150076, 'Start_Date': '2024-10-01', 'End_Date': '2024-10-01', 'Time': 'FULL DAY', 'Status': 'Approved'}]

    result = build_events(sample_data)

    assert result[0]['id'] == '1_2024-10-01'