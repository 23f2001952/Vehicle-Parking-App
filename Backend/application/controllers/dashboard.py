from flask import current_app as app, jsonify,abort,request
from application.models import User,ParkingLot
from flask_jwt_extended import create_access_token,current_user,jwt_required
from application.middlewares import role_required

@role_required('admin')
def admin_dashboard():
    users = User.query.filter_by(role='user').all()
    parking_lots = ParkingLot.query.all()
    parking_spots = parking_lots.spots
    return jsonify({
        "msg" : "welcome to Admin dashboard",
        "username" : current_user.username,
        "email"     : current_user.email
    })

@role_required('user')
def user_dashboard():
    return jsonify({
        "msg" : f"welcome to {current_user.username} dashboard",
        "username" : current_user.username,
        "email"     : current_user.email
    })