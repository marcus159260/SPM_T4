from flask import Blueprint, jsonify, request
from controllers.user_controller import *
from util.auth_decorators import login_required, role_required

user_bp = Blueprint('user_bp', __name__)

# @user_bp.route('/', methods=['GET'])
# def users():
#     users = get_all_users_names()
#     if users:
#         return jsonify(users)
#     else:
#         return jsonify({'error': 'Users not found'}), 404


@user_bp.route('/', methods=['GET'])
# @login_required
# @role_required(['1'])
def get_all_users():
    user_data = get_all_users_data()  
    if user_data:
        return jsonify({"status": "success", "data": user_data}), 200 
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
    
@user_bp.route('/get-manager/<int:manager_id>', methods=['GET'])
def get_manager_details(manager_id):
    manager = get_manager_details_data(manager_id)
    if manager:
        return jsonify({"status": "success", "data": manager}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    

@user_bp.route('/find-manager/<int:staff_id>', methods=['GET'])
def find_manager_details(staff_id):
    manager = find_manager_details_data(staff_id)
    if manager:
        return jsonify({"status": "success", "data": manager}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
@user_bp.route('/by-dept-employees', methods=['GET'])
def get_employees_by_dept():
    user = get_employees_by_dept_data() 
    if user:
        return jsonify({"status": "success", "data": user}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    

@user_bp.route('/resources', methods=['GET'])
@login_required
@role_required([1])
def get_resources_endpoint():
    resources = get_resources()
    if resources is None:
        return jsonify({'error': 'Failed to fetch employee data'}), 500
    return jsonify(resources)

@user_bp.route('/all-staff-under-manager/<int:reporting_manager_id>', methods=['GET'])
def get_all_staff_under_manager(reporting_manager_id):
    resources = get_all_employees_below_reporting_manager(reporting_manager_id)
    print(jsonify(resources))
    if resources == []:
        return jsonify({'error': 'Failed to fetch employee data'}), 404
    return jsonify({"status": "success", "data": resources}), 200

@user_bp.route('/by-team-employees/<int:reporting_manager_id>', methods=['GET']) #test-case: 140894
# @login_required
# @role_required(['2'])
def get_employees_by_team(reporting_manager_id):
    team = get_employees_by_reporting_manager(reporting_manager_id) 
    resources = []
    for emp in team:
        resources.append({"name":emp['Staff_FName']+" " +emp['Staff_LName'],"id":emp['Staff_ID'],"Dept":emp['Dept'],"Position":emp['Position']})

    if team:
        return jsonify({"status": "success", "data": resources}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404
    
@user_bp.route('/department_counts', methods=['GET'])
# @login_required
# @role_required([1])
def get_department_counts():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    counts = get_department_wfh_wfo_counts(start_date, end_date)
    # counts = None
    if counts is None:
        return jsonify({'error': 'Failed to fetch department counts'}), 500
    return jsonify(counts), 200