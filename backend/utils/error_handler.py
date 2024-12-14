from functools import wraps
from flask import jsonify
import traceback

def handle_error(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            # Log the full traceback for debugging
            print(traceback.format_exc())
            # Return a generic error message to the client
            return jsonify({
                'error': 'An internal server error occurred',
                'message': str(e)
            }), 500
    return decorated_function
