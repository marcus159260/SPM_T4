from flask import Blueprint, jsonify
from controllers.user_controller import get_all_users

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def users():
    return jsonify(get_all_users())
