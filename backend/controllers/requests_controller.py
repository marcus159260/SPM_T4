from util.db import supabase
from datetime import datetime, timedelta


# Get all the requests from a specific user id (staff)
def get_staff_requests_data(user_id):
    response = (supabase.table('request').select('*').eq('Staff_ID', user_id).execute())
    if response.data:
        return response.data
        return result
    else:
        return None

def get_staff_events_data(staff_id):
    try:
        response = supabase.table('request').select(
            'Request_ID',
            'Staff_ID',
            'Start_Date',
            'End_Date',
            'Time',
            'Status'
        ).eq('Staff_ID', staff_id).execute()
        data = response.data
    except Exception as e:
        print(f"Error fetching events data: {e}")
        return None

    events = build_events(data)
    return events

def get_all_events_data():
    try:
        response = supabase.table('request').select(
            'Request_ID',
            'Staff_ID',
            'Start_Date',
            'End_Date',
            'Time',
            'Status'
        ).execute()
        data = response.data
    except Exception as e:
        print(f"Error fetching events data: {e}")
        return None

    events = build_events(data)
    return events

def build_events(data):
    events = []

    for row in data:
        request_id = row['Request_ID']
        staff_id = row['Staff_ID']
        start_date = row['Start_Date']  
        end_date = row['End_Date']      
        time_slot = row['Time']         
        status = row['Status']         

        if status != 'Approved':
            continue

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        date_range = [start_date_obj + timedelta(days=i) for i in range((end_date_obj - start_date_obj).days + 1)]

        for single_date in date_range:
            if time_slot == 'AM':
                start_time = '09:00:00'
                end_time = '13:00:00'
            elif time_slot == 'PM':
                start_time = '14:00:00'
                end_time = '18:00:00'
            elif time_slot == 'FULL DAY':
                start_time = '09:00:00'
                end_time = '18:00:00'
            else:
                print(f"Unknown time slot: {time_slot}")
                continue

            date_str = single_date.strftime('%Y-%m-%d')
            start = f"{date_str}T{start_time}"
            end = f"{date_str}T{end_time}"

            event_id = f"{request_id}_{date_str}"

            event = {
                'id': event_id,
                'start': start,
                'end': end,
                'text': 'WFH', 
                'resource': f"E_{staff_id}", 
            }
            events.append(event)

    return events

def withdraw_request_controller(request_id, rejection_reason, staff_id):

    if not request_id or not rejection_reason:
        return {'error': 'Invalid input'}, 400

    response = supabase.table('request').select('*').eq('Request_ID', request_id).single().execute()
    request_data = response.data

    if not request_data:
        return {'error': 'Request not found'}, 404

    if request_data['Staff_ID'] != staff_id:
        return {'error': 'Unauthorized' }, 403

    start_date = datetime.strptime(request_data['Start_Date'], '%Y-%m-%d').date()
    end_date = datetime.strptime(request_data['End_Date'], '%Y-%m-%d').date()
    today = datetime.today().date()
    two_weeks_ago = today - timedelta(days=14)
    two_weeks_later = today + timedelta(days=14)

    if not (two_weeks_ago <= start_date <= two_weeks_later):
        return {'error': 'Cannot withdraw request outside the allowed time frame'}, 400

    supabase.table('request').update({
        'Status': 'Withdrawn',
        'Rejection_Reason': rejection_reason
    }).eq('Request_ID', request_id).execute()

    return {'message': 'Request withdrawn successfully'}, 200
