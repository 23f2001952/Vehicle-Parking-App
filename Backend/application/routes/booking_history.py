from flask import Blueprint
from application.controllers.booking_history import get_booking_history_by_user,get_booking_history_all,get_booking_analytics_per_parking_lot

booking_history_bp = Blueprint('booking_history', __name__)

booking_history_bp.add_url_rule('/get', methods=['GET'], view_func=get_booking_history_by_user)
booking_history_bp.add_url_rule('/get_all', methods=['GET'], view_func=get_booking_history_all, endpoint='get_booking_history_all')
booking_history_bp.add_url_rule('/analytics', methods=['GET'], view_func=get_booking_analytics_per_parking_lot)