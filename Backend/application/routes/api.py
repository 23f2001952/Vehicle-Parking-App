from flask import Blueprint
from .auth import auth_bp
from .dashboard import dashboard_bp
from .parking_lot import parking_lot_bp
from .parking_spot import parking_spot_bp
from .booking_history import booking_history_bp
from application.tasks import user_csv_report, monthly_report, generate_msg
from celery.result import AsyncResult
api_bp = Blueprint("api",__name__)


def test():
    result= user_csv_report.delay()
    return 
    {
        "result":result.result
    }
api_bp.register_blueprint(auth_bp,url_prefix='/auth')
api_bp.register_blueprint(dashboard_bp,url_prefix='/dashboard')
api_bp.register_blueprint(parking_lot_bp,url_prefix='/parking_lot')
api_bp.register_blueprint(parking_spot_bp,url_prefix='/parking_spot')
api_bp.register_blueprint(booking_history_bp,url_prefix='/booking_history')

api_bp.add_url_rule('/tasks/user_csv_report', view_func=user_csv_report, methods=['GET'])
api_bp.add_url_rule('/tasks/monthly_report', view_func=monthly_report, methods=['GET'])
api_bp.add_url_rule('/tasks/generate_msg', view_func=generate_msg, methods=['GET'])


