from flask import Blueprint, request, jsonify
from backend.utils.error_handler import handle_error
from functools import wraps

user_bp = Blueprint('user', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Add authentication logic here
        return f(*args, **kwargs)
    return decorated_function

@user_bp.route('/login', methods=['POST'])
@handle_error
def login():
    data = request.get_json()
    # Add login logic here
    return jsonify({'message': 'Login successful'}), 200

@user_bp.route('/register', methods=['POST'])
@handle_error
def register():
    data = request.get_json()
    # Add registration logic here
    return jsonify({'message': 'Registration successful'}), 201
