# routes/wfh_routes.py
from flask import Blueprint, jsonify
from config import supabase  # Import the Supabase client from config

wfh_bp = Blueprint('wfh_bp', __name__)

@wfh_bp.route('/requests', methods=['GET'])
def get_wfh_requests():
        # Fetch WFH requests from Supabase
        response = supabase.table('request').select('*').execute()

        if response.data is not None:
            return jsonify(response.data),200
        else:
            return jsonify({"error":response.error}),400 # Return the actual data


