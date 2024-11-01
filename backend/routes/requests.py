# routes/wfh_routes.py
from flask import Blueprint, jsonify, request
from controllers.requests_controller import *
from util.db import supabase 
from util.auth_decorators import login_required, role_required

wfh_bp = Blueprint('wfh_bp', __name__)

@wfh_bp.route('/requests', methods=['GET'])
def get_wfh_requests():
    try:
        auto_reject_pending_requests()
        
        # Call the function to fetch the data
        data, error = supabase.rpc('get_requests').execute()

        if error[0] != 'count':
            return jsonify({"error": f"Error fetching data: {error}"}), 500
        else:
            return jsonify(data[1])  # Return the actual data
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
@login_required
@role_required([1])
def get_all_events():
    events = get_all_events_data()
    if events is None:
        return jsonify({'error': 'Failed to fetch events data'}), 500
    return jsonify(events)

@wfh_bp.route('/events/<int:staff_id>', methods=['GET'])
def get_events_for_current_user(staff_id):
    # print(staff_id)
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
    
@wfh_bp.route('/requests/approver/<int:approver_id>', methods=['GET'])
def get_requests_by_approver(approver_id):
    try:
        # Call the Supabase RPC function
        response = supabase.rpc('get_requests_by_approver', {'approver_id': approver_id}).execute()

        # Check if there's an error in the SQL response
        if len(response.data) > 0 and response.data[0]['Error']:
            return jsonify({'error': response.data[0]['Error']}), 400

        # Return the request data
        return jsonify(response.data), 200

    except Exception as e:
        # Catch any unexpected errors and return a 500 response
        return jsonify({'error': str(e)}), 500
    
@wfh_bp.route('/requests/withdraw', methods=['POST'])
def withdraw_request():
    data = request.get_json()
    request_id = data.get('Request_ID')
    rejection_reason = data.get('Rejection_Reason')
    staff_id = data.get('Staff_ID'); 
    result, status_code = withdraw_request_controller(request_id, rejection_reason, staff_id)
    if status_code == 200:
        log_activity(
                request_id = data.get('Request_ID'),
                old_status = 'Approved',
                new_status = 'Withdrawn - Pending',
                changed_by = data.get('Staff_ID'),
                change_message = 'Request withdrawn successfully',
                reason =  rejection_reason 
            )
    return jsonify(result), status_code

@wfh_bp.route('/requests', methods=['POST'])
def create_request():
    try:
        data = request.get_json()

        staff_id = data.get('staff_id')
        start_date = str(data.get('start_date'))
        end_date = str(data.get('end_date'))
        time_of_day = data.get('time_of_day')
        request_type = data.get('request_type')
        status = data.get('status')
        reason = data.get('reason').replace("'", "''") 
        approver_id = data.get('approver_id')
        requested_dates = [str(date) for date in data.get('requested_dates')]

        conflict_response = check_conflict(staff_id, requested_dates, time_of_day)

        if conflict_response.data and conflict_response.data != 'No conflict':
            return jsonify({'error': conflict_response.data}), 400  # Return conflict message

        # if no conflict, proceed to create request
        response = supabase.rpc('create_request', {
            'p_staff_id': staff_id,
            'p_start_date': start_date,
            'p_end_date': end_date,
            'p_time': time_of_day,
            'p_request_type': request_type,
            'p_status': status,
            'p_reason': reason,
            'p_approver_id': approver_id,
            'p_requested_dates': requested_dates 
        }).execute()

        if response.data and isinstance(response.data, list) and len(response.data) > 0:
            first_request_id = response.data[0]['first_request_id']
            message = response.data[0]['message']

            log_response = log_activity(
                request_id = first_request_id,
                old_status = None,
                new_status = status,
                changed_by = staff_id,
                change_message = 'Request created successfully',
                reason = reason
            )

            if log_response.data is None: 
                print("Error logging activity: No data in log response")
            else:
                print("Activity logged successfully:", log_response.data)

            return jsonify({'first_request_id': first_request_id, 'message': message}), 201
        
        return jsonify({'error': 'Unable to create request'}), 401

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500


@wfh_bp.route('/requests/cancel', methods=['POST'])
def cancel_request():
    data = request.get_json()
    request_id = data.get('Request_ID')
    reason = data.get('Withdrawal_Reason')
    staff_id = data.get('Staff_id')

    if not request_id or not reason:
        return jsonify({'error': 'Request ID and reason are required.'}), 400

    # Call the controller to handle the business logic
    result = cancel_wfh_request(request_id, reason, staff_id)
    
    return jsonify(result), result['status']

@wfh_bp.route('/requests/approve', methods=['POST'])
def update_request():
    try:
        request_data = request.json
        request_id = request_data.get('Request_ID')
        status = request_data.get('request_Status')
        force_approval = request_data.get('force_approval', False) 
        
        # print(request_id, status)
        if not request_id or not status:
            return jsonify({"error": "Missing request ID or status"}), 400
        result, status_code = approve_wfh_request(request_id, status, force_approval)
        print("result, status code:", result, status_code)
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wfh_bp.route('/requests/approvewithdrawal', methods=['POST'])
def approve_withdrawal_request():
    try:
        request_data = request.json
        print(request_data)
        request_id = request_data.get('Request_ID')
        
        # print(request_id, status)
        if not request_id:
            return jsonify({"error": "Missing request ID"}), 400
        result, status_code = approve_withdrawal_wfh_request(request_id)
     
        return jsonify(result), status_code
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@wfh_bp.route('/requests/reject', methods=['POST'])
def reject_request():
    data = request.get_json()
    request_id = data.get('Request_ID')
    rejection_reason = data.get('Rejection_Reason')
    result, status_code = reject_wfh_request(request_id, rejection_reason)
    return jsonify(result), status_code

@wfh_bp.route('/requests/rejectwithdrawal', methods=['POST'])
def reject_withdrawal_request():
    data = request.get_json()
    print(123456)
    request_id = data.get('Request_ID')
    rejection_reason = data.get('Withdrawal_Reason')
    result, status_code = reject_wfh_withdrawal_request(request_id, rejection_reason)
    
    return jsonify(result), status_code
