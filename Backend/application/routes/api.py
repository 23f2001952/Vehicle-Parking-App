from flask import Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .parking_lot import parking_lot_bp

api_bp = Blueprint("api",__name__)

api_bp.register_blueprint(auth_bp,url_prefix='/auth')
api_bp.register_blueprint(dashboard_bp,url_prefix='/dashboard')
api_bp.register_blueprint(parking_lot_bp,url_prefix='/parking_lot')
