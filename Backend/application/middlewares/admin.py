from flask import jsonify
from flask_jwt_extended import jwt_required,current_user
from functools import wraps

def role_required(required_role):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify("Not Authorized"),403
            return fn(*args, **kwargs)
        return wrapper
    return decorator