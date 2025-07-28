
from flask import Blueprint
from application.controllers.dashboard import admin_dashboard

dashboard_bp = Blueprint('dashboard',__name__)

dashboard_bp.add_url_rule('/admin',methods=['GET'],view_func=admin_dashboard)