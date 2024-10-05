# routes/wfh_routes.py
from flask import Blueprint, jsonify
from controllers.requests_controller import *
# from config import supabase  # Import the Supabase client from config
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
   
@wfh_bp.route('/<int:user_id>', methods=['GET']) 
def get_staff_requests(user_id):
    requests = get_staff_requests_data(user_id)
    if requests:
        return jsonify({"status": "success", "data": requests}), 200
    else:
        return jsonify({"status": "error", "message": f"Requests for {user_id} not found"}), 200