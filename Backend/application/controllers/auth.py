from flask import current_app as app, jsonify,abort,request
from application.models import User, BookingHistory,ParkingLot
from application.middlewares import role_required
from flask_jwt_extended import create_access_token,current_user,jwt_required
from werkzeug.security import generate_password_hash,check_password_hash
from application.database import db

def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(username=username).one_or_none()

    if not user:
        return jsonify('No user found'),401
    if check_password_hash(user.password,password) == False :
        return jsonify('Incorrect password!'),401

    access_token=create_access_token(identity=user)
    role = user.role
    return jsonify(access_token=access_token,role=role)

def register():

    username = request.json.get("username",None)
    email = request.json.get("email",None)
    password = request.json.get("password",None)
    confirm_password = request.json.get("confirm_password",None)
    address = request.json.get("address", None)
    pincode = request.json.get("pincode", None)

    if not username:
        return jsonify('Username Required'),401
    if not email:
        return jsonify('email Required'),401
    if not password:
        return jsonify('Password Required'),401
    if not confirm_password:
        return jsonify('Confirm Password Required'),401
    if password != confirm_password:
        return jsonify("Confirm password and passowrd doesn't match"),401
    if not address:
        return jsonify('Address Required'), 401
    if not pincode:
        return jsonify('Pincode Required'), 401
    
    user = User.query.filter_by(username=username).one_or_none()

    if user:
        return jsonify('Username already exists enter an different username'),401
    
    user = User.query.filter_by(email=email).one_or_none()

    if user:
        return jsonify('email already exists enter an different email'),401

    db.session.add(User(username=username, email=email, password=generate_password_hash(password), address=address, pincode=pincode))
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@role_required('admin')
def get_all_users():
    users = User.query.filter(User.role != 'admin').all()
    if not users:
        return jsonify({"msg": "No users found"}), 404
    users_json = []
    for user in users:
        user_json = {}
        user_json["id"] = user.id
        user_json["username"] = user.username
        user_json["email"] = user.email
        user_json["role"] = user.role
        user_json["address"] = user.address if user.address else None
        user_json["pincode"] = user.pincode if user.pincode else None  
        users_json.append(user_json)
    return jsonify({"Users": users_json})

@role_required('admin')
def get_user_by_id(id):
    user = User.query.get(id)
    if not user:
        abort(404, description="User not found.")

    history = BookingHistory.query.filter_by(user_id=user.id).all()
    if not history:
        history=[]
    
    history_json = []
    for booking in history:
        booking_json = {
            "id": booking.id,
            "spot_id": booking.spot_id,
            "vehicle_number": booking.vehicle_number,
            "user_id": booking.user_id,
            "start_time": booking.start_time.isoformat() if booking.start_time else None,
            "end_time": booking.end_time.isoformat() if booking.end_time else None,
            "parking_cost": str(booking.parking_cost) if booking.parking_cost else None,
            "is_paid": booking.is_paid,
            "location": booking.spot.lots.prime_location_name if booking.spot and booking.spot.lots else None
        }
        history_json.append(booking_json)
    user_json = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "address": user.address if user.address else None,
        "pincode": user.pincode if user.pincode else None,
        "history": history_json
    }
    return jsonify(data=user_json), 200

@jwt_required()
def whoami():
    user = current_user
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user_json = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role,
    }
    return jsonify(user_json), 200

@role_required('user')
def get_user_analytics():
    user = current_user
    if not user:
        return jsonify({"msg": "User not found"}), 404

    history = BookingHistory.query.filter_by(user_id=user.id).all()
    if not history:
        return jsonify({"msg": "No booking history found"}), 404

    total_cost = sum(booking.parking_cost or 0 for booking in history)

 
    parking_lot_ids = {
        booking.spot.lots.id
        for booking in history
        if booking.spot and booking.spot.lots
    }

    if not parking_lot_ids:
        return jsonify({"msg": "No parking lot bookings found"}), 404

    lot_cost_dict = {}
    for lot_id in parking_lot_ids:
        lot = ParkingLot.query.get(lot_id)
        if not lot:
            return jsonify({"msg": f"Parking lot with ID {lot_id} not found"}), 404

        lot_cost = sum(
            booking.parking_cost or 0
            for booking in history
            if booking.spot and booking.spot.lots and booking.spot.lots.id == lot_id
        )
        lot_cost_dict[lot_id] = f"{lot_cost:.2f}"

    analytics = {
        "user_id": user.id,
        "username": user.username,
        "total_bookings": len(history),
        "total_cost": f"{total_cost:.2f}",
        "parking_lot_ids": list(parking_lot_ids),
        "lot_costs": lot_cost_dict,
    }

    return jsonify(data=analytics), 200
