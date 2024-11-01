from functools import wraps
from flask import request, jsonify

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        staff_id = request.headers.get('X-Staff-ID')
        if not staff_id:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def role_required(required_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            staff_id = request.headers.get('X-Staff-ID')
            role = request.headers.get('X-Staff-Role')
            if not staff_id or not role:
                return jsonify({'error': 'Proper role required'}), 401
            try:
                role = int(role)
            except ValueError:
                return jsonify({'error': 'Invalid role format'}), 400
            if role not in required_roles:
                return jsonify({'error': 'Forbidden'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator