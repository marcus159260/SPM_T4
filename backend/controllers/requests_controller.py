from util.db import supabase
from datetime import datetime, timedelta

def get_staff_requests_data(user_id):
    response = supabase.table('request').select('*').eq('Staff_ID', user_id).execute()
    if response.data:
        return response.data
    else:
        return None
    
def get_staff_events_data():
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
                start_time = '08:00:00'
                end_time = '12:00:00'
            elif time_slot == 'PM':
                start_time = '13:00:00'
                end_time = '18:00:00'
            elif time_slot == 'Full Day':
                start_time = '08:00:00'
                end_time = '18:00:00'
            # else:
            #     print(f"Unknown time slot: {time_slot}")
            #     continue

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
