from flask import Blueprint
from application.controllers.auth import login,register,get_all_users,get_user_by_id,get_user_analytics
from flask_jwt_extended import jwt_required

auth_bp = Blueprint('auth',__name__)

auth_bp.add_url_rule('/login',methods=['POST'],view_func=login)
auth_bp.add_url_rule('/register',methods=['POST'],view_func=register)
auth_bp.add_url_rule('/users',methods=['GET'],view_func=get_all_users)
auth_bp.add_url_rule('/users/<int:id>',methods=['GET'],view_func=get_user_by_id)
auth_bp.add_url_rule('/analytics', methods=['GET'], view_func=get_user_analytics)