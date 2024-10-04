from flask import Blueprint, jsonify, request
from controllers.user_controller import *

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def users():
    users = get_all_users_names()
    if users:
        return jsonify(users)
    else:
        return jsonify({'error': 'Users not found'}), 404


@user_bp.route('/', methods=['GET'])
def get_all_users():
    user_data = get_all_users_data()  # Fetch user data from Supabase
    if user_data:
        return jsonify({"status": "success", "data": user_data}), 200  # Return JSON response with the user data
    else:
        return jsonify({"status": "error", "message": "No data found"}), 404

# Route to get a single user by ID (e.g 140001)
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = get_user_data_by_id(user_id)  # Call a function to fetch a specific user
    if user:
        return jsonify({"status": "success", "data": user}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
@user_bp.route('by-dept-employees', methods=['GET']) #test-case: 150245
def get_employees_by_dept():
    user = get_employees_by_dept_data() 
    if user:
        return jsonify({"status": "success", "data": user}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
@user_bp.route('/resources', methods=['GET'])
def get_resources_endpoint():
    resources = get_resources()
    if resources is None:
        return jsonify({'error': 'Failed to fetch employee data'}), 500
    return jsonify(resources)