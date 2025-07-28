from flask import Blueprint
from application.controllers.auth import login,register,whoami
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth',__name__)

auth_bp.add_url_rule('/login',methods=['POST'],view_func=login)
auth_bp.add_url_rule('/register',methods=['POST'],view_func=register)
auth_bp.add_url_rule('/who-am-i',methods=['GET'],view_func=whoami)