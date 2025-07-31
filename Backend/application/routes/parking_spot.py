from flask import Blueprint
from application.controllers.parking_spot import get_parking_spot,release_parking_spot,get_parking_spot_by_id,book_parking_spot_by_lot_id,get_parking_spot_by_lot_id

parking_spot_bp = Blueprint('parking_spot',__name__)

parking_spot_bp.add_url_rule('/get',methods=['GET'],view_func=get_parking_spot)
parking_spot_bp.add_url_rule('/get/<int:id>',methods=['GET'],view_func=get_parking_spot_by_id)
parking_spot_bp.add_url_rule('/update/<int:id>',methods=['PUT'],view_func=release_parking_spot)
parking_spot_bp.add_url_rule('/book/<int:lot_id>',methods=['POST'],view_func=book_parking_spot_by_lot_id)
parking_spot_bp.add_url_rule('/get_by_plot/<int:lot_id>',methods=['GET'],view_func=get_parking_spot_by_lot_id)
