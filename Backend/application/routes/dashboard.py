
from flask import Blueprint
from application.controllers.dashboard import admin_dashboard,user_dashboard

dashboard_bp = Blueprint('dashboard',__name__)

dashboard_bp.add_url_rule('/admin',methods=['GET'],view_func=admin_dashboard)
dashboard_bp.add_url_rule('/user',methods=['GET'],view_func=user_dashboard)