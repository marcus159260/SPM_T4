from util.db import supabase
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


# Get all the requests from a specific user id (staff)
def get_staff_requests_data(user_id):
    response = (supabase.table('request').select('*').eq('Staff_ID', user_id).execute())
    if response.data:
        return response.data
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
    two_weeks_ago = start_date - timedelta(days=14)
    two_weeks_later = end_date + timedelta(days=14)

    if not (two_weeks_ago <= today <= two_weeks_later):
        return {'error': 'Cannot withdraw request outside the allowed time frame'}, 400

    supabase.table('request').update({
        'Status': 'Withdrawn',
        'Withdrawal_Reason': rejection_reason
    }).eq('Request_ID', request_id).execute()

    return {'message': 'Request withdrawn successfully'}, 200


def cancel_wfh_request(request_id, reason, staff_id):
    try:
        # Fetch the request details by ID
        response = supabase.table('request').select("*").eq('Request_ID', request_id).execute()
        request_data = response.data[0]

        if not request_data:
            return {'error': 'Request not found.', 'status': 404}
        
        if request_data['Staff_ID'] != staff_id:
            return {'error': 'Unauthorized' }, 403

        #update status in database
        supabase.table('request').update({
        'Status': 'Withdrawn',
        'Withdrawal_Reason': reason
        }).eq('Request_ID', request_id).execute()

        return {'message': 'Request cancelled successfully.', 'status': 200}

    except Exception as e:
        return {'error': str(e), 'status': 500}
    
def auto_reject_pending_requests():
    try:
        current_date = datetime.now().date()
        # current_date = datetime(2025, 8, 8).date()

        # Fetch pending requests older than 2 months
        response = supabase.table('request').select("*").eq('Status', 'Pending').eq('Approver_ID', 151408).execute()
        pending_requests = response.data

        # Loop through the pending requests and auto-reject them if they exceed 2 months
        for request in pending_requests:
            start_date = request['Start_Date'] 
            # print(start_date)

            start_date_obj = datetime.strptime(start_date, "%Y-%m-%d").date()

            if current_date > start_date_obj + relativedelta(months=2):
                supabase.table('request').update({'Status': 'Rejected', 'Rejection_Reason': 'Auto-rejected after 2 months'}).eq('Request_ID', request['Request_ID']).execute()

    except Exception as e:
        print("Error in auto-rejecting requests:", str(e))

def approve_wfh_request(request_id, status):
    try:
        response = supabase.table('request').select("*").eq('Request_ID', request_id).execute()
        request_data = response.data[0] if response.data else None
        print(request_data)
        if not request_data:
            return {'error': 'Request not found.', 'status': 404}

        # current_date = datetime.now().date()
    # Check how many are currently approved for WFH between start_date and end_date
        # approved_wfh_response = supabase.table('request').select("*")\
        #     .eq('Status', 'Approved')\
        #     .lte('Start_Date', current_date)\
        #     .gte('End_Date', current_date).execute()
        
        # approved_wfh_count_db = len(approved_wfh_response.data)
        # print(approved_wfh_count_db)

        approved_wfh_count = 5
        # print("approved count:", approved_wfh_count)
        
        current_working_in_office = 10 #hardcode 
        validation = (approved_wfh_count + 1) / current_working_in_office
        # print("validation:", validation)
        if validation > 0.5:
            return {'error': 'Cannot approve request as less than 50% of the team will be in the office.', 'status': 400}   

        else:
            update_response = supabase.table('request').update({'Status': status}).eq('Request_ID', request_id).execute()
            print("Update response:", update_response)
            return {"message": "Request approved successfully."}, 200

    except Exception as e:
        return {"error": str(e)}, 500

def reject_wfh_request(request_id, reason, date_to_cancel=None):
    try:
        # Fetch the request details by ID
        response = supabase.table('request').select("*").eq('Request_ID', request_id).execute()
        request_data = response.data[0]

        if not request_data:
            return {'error': 'Request not found.', 'status': 404}
        
        if reason == '':
            return {'error': 'Reason cannot be empty.', 'status': 404}
        # Handle adhoc vs recurring request
        update_response = supabase.table('request').update({
        'Status': 'Rejected',
        'Rejection_Reason': reason
        }).eq('Request_ID', request_id).execute()
        
        print(update_response)  # Check if update was successful

        return {'message': 'Request cancelled successfully.', 'status': 200}

    except Exception as e:
        return {'error': str(e), 'status': 500}