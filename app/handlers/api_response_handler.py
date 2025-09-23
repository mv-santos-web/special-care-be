from flask import jsonify
from werkzeug.exceptions import HTTPException
from functools import wraps

def handle_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return jsonify({"success": True, "data": response}), 200
        except HTTPException as e:
            return jsonify({"success": False, "message": str(e)}), e.code
        except Exception as e:
            return jsonify({"success": False, "message": str(e)}), 500
    return wrapper
