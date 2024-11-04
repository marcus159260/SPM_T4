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
    if user:
        return jsonify({'success': True, 'user': user}), 200
    else:
        return jsonify({'success': False, 'message': 'Invalid username or password'}), 401