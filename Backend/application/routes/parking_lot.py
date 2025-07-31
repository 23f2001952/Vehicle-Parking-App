from flask import Blueprint
from application.controllers.parking_lot import add_parking_lot,get_all_parking_lot,delete_parking_lot,get_parking_lot_by_id,update_parking_lot,get_available_spots_by_lot_id, get_parking_lot_analytics

parking_lot_bp = Blueprint('parking_lot',__name__)

parking_lot_bp.add_url_rule('/add',methods=['POST'],view_func=add_parking_lot)
parking_lot_bp.add_url_rule('/delete/<int:id>',methods=['DELETE'],view_func=delete_parking_lot)
parking_lot_bp.add_url_rule('/get/<int:id>',methods=['GET'],view_func=get_parking_lot_by_id,endpoint='get_parking_lot_by_id')
parking_lot_bp.add_url_rule('/get',methods=['GET'],view_func=get_all_parking_lot)
parking_lot_bp.add_url_rule('/update/<int:id>',methods=['PUT'],view_func=update_parking_lot)
parking_lot_bp.add_url_rule('/get_available_spots/<int:lot_id>',methods=['GET'],view_func=get_available_spots_by_lot_id)
parking_lot_bp.add_url_rule('/analytics', methods=['GET'], view_func=get_parking_lot_analytics)