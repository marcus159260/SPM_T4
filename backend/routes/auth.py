from flask import request, session, jsonify, Blueprint
from controllers.auth_controller import *
from util.db import supabase 

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    staff_id = data.get('Staff_ID')
    # get user data from supabase
    user = authenticate_user(staff_id)
    # store user data in session
    if user:
        # session['staff_id'] = user['staff_id']
        # session['role'] = user['role']
        # session['position'] = user['position']
        # session['department'] = user['department']
        # session['staff_fname'] = user['staff_fname']
        # session['staff_lname'] = user['staff_lname']
        # session['reporting_manager'] = user['reporting_manager']
        # print(user)
        return jsonify({'success': True, 'user': user}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401

# @auth_bp.route('/logout', methods=['POST'])
# def logout():
#     session.clear()
#     return jsonify({'success': True})

# @auth_bp.route('/check_auth', methods=['GET'])
# def check_auth():
#     if 'staff_id' in session:
#         return jsonify({
#             'authenticated': True,
#             'staff_id': session['staff_id'],
#             'role': session['role'],
#             'position': session['position'],
#             'department': session['department'],
#             'staff_fname': session['staff_fname'],
#             'staff_lname': session['staff_lname'],
#             'reporting_manager': session['reporting_manager']
#         })
#     else:
#         return jsonify({'authenticated': False})