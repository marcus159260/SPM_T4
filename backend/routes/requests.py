# routes/wfh_routes.py
from flask import Blueprint, jsonify, request
from controllers.requests_controller import *
from util.db import supabase 


wfh_bp = Blueprint('wfh_bp', __name__)


@wfh_bp.route('/requests', methods=['GET'])
def get_wfh_requests():
    try:
        # Call the function to fetch the data
        data, error = supabase.rpc('get_requests').execute()

        if error[0] != 'count':
            return jsonify({"error": f"Error fetching data: {error}"}), 500
        else:
            return jsonify(data[1])  # Return the actual data
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wfh_bp.route('/requests/<int:request_id>', methods=['PUT'])
def update_request(request_id):
    print(request_id)
    try:
        # Get the status from the request body
        request_data = request.json
        status = request_data.get('Status')  # Get the 'Status' value from the request body
        print(status)

        # Assuming you have a Supabase method for updating the request status
        response = supabase.from_('request').update({'Status': status}).eq('Request_ID', request_id).execute()

        print(response)
        if response.error:
            return jsonify({"error": response.error.message}), 500
        
        return jsonify({"status": "success", "data": response.data}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


   
#------------------------------------------------------------------------------
   
@wfh_bp.route('/<int:user_id>', methods=['GET']) 
def get_staff_requests(user_id):
    requests = get_staff_requests_data(user_id)
    if requests:
        return jsonify({"status": "success", "data": requests}), 200
    else:
        return jsonify({"status": "error", "message": f"Requests for {user_id} not found"}), 200
    
@wfh_bp.route('/all_events', methods=['GET'])
def get_all_events():
    events = get_all_events_data()
    if events is None:
        return jsonify({'error': 'Failed to fetch events data'}), 500
    return jsonify(events)

@wfh_bp.route('/events/<int:staff_id>', methods=['GET'])
def get_events_for_current_user(staff_id):
    # staff_id = session.get('staff_id')
    if not staff_id:
        return jsonify({'error': 'Unauthorized'}), 401

    events = get_staff_events_data(staff_id)
    if events is None:
        return jsonify({'error': 'Failed to fetch events data'}), 500
    return jsonify(events)

@wfh_bp.route('/requests/<int:user_id>', methods=['GET'])
def get_user_req(user_id):
    try:
        # Call the Supabase stored procedure with the user_id as a parameter
        response = supabase.rpc('get_user_requests', {"p_staff_id": user_id}).execute()

        # Check if the response has errors based on the 'status' or 'data'
        if response.data:
            return jsonify(response.data), 200
        else:
            # Handle cases where there is an error or no data
            return jsonify({"error": response.error.message if response.error else "No data found"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wfh_bp.route('/requests/withdraw', methods=['POST'])
def withdraw_request():
    data = request.get_json()
    request_id = data.get('Request_ID')
    rejection_reason = data.get('Rejection_Reason')
    staff_id = data.get('Staff_ID'); 
    result, status_code = withdraw_request_controller(request_id, rejection_reason, staff_id)
    return jsonify(result), status_code

@wfh_bp.route('/requests', methods=['POST'])
def create_request():
    try:
        data = request.get_json()

        # Parse and validate date fields
        staff_id = data.get('staff_id')
        start_date = str(datetime.strptime(data.get('start_date'), '%Y-%m-%d').date())
        end_date = str(datetime.strptime(data.get('end_date'), '%Y-%m-%d').date())
        time_of_day = data.get('time_of_day')
        request_type = data.get('request_type')
        status = data.get('status')
        reason = data.get('reason').replace("'", "''")  # Escape single quotes
        approver_id = data.get('approver_id')
        requested_dates = [str(datetime.strptime(date, '%Y-%m-%d').date()) for date in data.get('requested_dates')]

        # Call the stored procedure with the validated data
        response = supabase.rpc('create_request', {
            'p_staff_id': staff_id,
            'p_start_date': start_date,
            'p_end_date': end_date,
            'p_time': time_of_day,
            'p_request_type': request_type,
            'p_status': status,
            'p_reason': reason,
            'p_approver_id': approver_id,
            'p_requested_date': requested_dates
        }).execute()

        # Check if there's an error in the response
        if response.data[1][0] == "Request created successfully":
            return jsonify({'message': response.data[1][0]}), 200

        return jsonify({'error': 'Unable to create request'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

