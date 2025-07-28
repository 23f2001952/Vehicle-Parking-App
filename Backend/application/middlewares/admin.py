from flask import jsonify
from flask_jwt_extended import jwt_required,current_user
from functools import wraps

def role_required(required_role):
    def wrapper(fn):
        @jwt_required()
        @wraps(fn)
        def decorator(*args, **kwargs):
            if current_user.role != required_role:
                return jsonify("Not Authorized"),403
            return fn(*args, **kwargs)
        return decorator
    return wrapper