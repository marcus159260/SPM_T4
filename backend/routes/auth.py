from flask import request, session, jsonify, Blueprint
from controllers.auth_controller import *
from util.db import supabase 
auth_bp = Blueprint('auth_bp', __name__)
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    staff_id = data.get('Staff_ID')
    user = authenticate_user(staff_id)
    if user:
        session['staff_id'] = user['staff_id']
        session['role'] = user['role']
        session['position'] = user['position']
        session['department'] = user['department']
        session['staff_fname'] = user['staff_fname']
        session['staff_lname'] = user['staff_lname']
        session['reporting_manager'] = user['reporting_manager']
        print(session)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})
@auth_bp.route('/check_auth', methods=['GET'])
def check_auth():
    if 'user_id' in session:
        return jsonify({'authenticated': True, 'role': session.get('role')})
    else:
        return jsonify({'authenticated': False})