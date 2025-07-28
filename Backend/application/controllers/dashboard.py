from flask import current_app as app, jsonify,abort,request
from application.models import User
from flask_jwt_extended import create_access_token,current_user,jwt_required
from application.middlewares import role_required

@role_required('admin')
def admin_dashboard():
    return jsonify("Welcome to admin dashboard")
