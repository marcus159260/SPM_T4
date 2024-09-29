from flask import Blueprint, jsonify,request
from controllers.user_controller import get_all_users_names, get_user_by_id

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def users():
    users = get_all_users_names()
    if users:
        return jsonify(users)
    else:
        return jsonify({'error': 'Users not found'}), 404

