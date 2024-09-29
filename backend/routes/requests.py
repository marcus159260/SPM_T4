# routes/wfh_routes.py
from flask import Blueprint, jsonify
from config import supabase  # Import the Supabase client from config

wfh_bp = Blueprint('wfh_bp', __name__)

@wfh_bp.route('/requests', methods=['GET'])
def get_wfh_requests():
    try:
        # Fetch WFH requests from Supabase
        data, error = supabase.from_('request').select('*').execute()

        if error[0] != 'count':
            return jsonify({"error": f"Error connecting to Supabase: {error}"}), 500
        else:
            return jsonify(data[1])  # Return the actual data
    except Exception as e:
        return jsonify({"error": str(e)}), 500

