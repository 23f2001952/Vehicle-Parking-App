from flask import Blueprint
from application.controllers.parking_spot import get_parking_spot,add_parking_spot,remove_parking_spot,update_parking_spot,get_parking_spot_by_id

parking_spot_bp = Blueprint('parking_spot',__name__)

parking_spot_bp.add_url_rule('/get',methods=['GET'],view_func=get_parking_spot)
parking_spot_bp.add_url_rule('/get/<int:id>',methods=['GET'],view_func=get_parking_spot_by_id)
parking_spot_bp.add_url_rule('/add',methods=['POST'],view_func=add_parking_spot)