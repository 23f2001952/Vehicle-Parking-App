from flask import jsonify, abort,request
from application.models import ParkingSpot,BookingHistory
from application.database import db
from flask_jwt_extended import  current_user,jwt_required
from application.middlewares import role_required
from datetime import datetime


def get_parking_spot():
    parking_spots = ParkingSpot.query.all()
    parking_spots_json = []
    for spot in parking_spots:
        parking_spot = {
            "id": spot.id,
            "lot_id": spot.lot_id,
            "status": spot.status
        }
        parking_spots_json.append(parking_spot)

    return jsonify({"ParkingSpots": parking_spots_json}), 200

@role_required('user')
def book_parking_spot_by_lot_id(lot_id):
    spot = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').first()
    print(f"Booking parking spot for lot_id: {lot_id}, found spot: {spot}")
    username = current_user.username
    email = current_user.email
    vehicle_number = request.json.get("vehicle_number", None)
    if not spot:
        abort(404, description="Parking Spot not found or all spots are occupied")
    spot.status = 'occupied'
    db.session.commit() 
    history = BookingHistory(spot_id=spot.id, user_id=current_user.id, vehicle_number=vehicle_number)
    db.session.add(history)
    db.session.commit()
    return jsonify({
        "msg": f"Parking Spot {spot.id} booked successfully by {username} ({email})"
    }), 201

@jwt_required()
def get_parking_spot_by_id(id):
    spot = ParkingSpot.query.get(id)
    if not spot:
        abort(404, description="Parking Spot not found")

    history = BookingHistory.query.filter_by(spot_id=spot.id).all()
    return jsonify({
        "id": spot.id,
        "lot_id": spot.lot_id,
        "status": spot.status,
        "price": spot.lots.price,
        "prime_location_name": spot.lots.prime_location_name if spot.lots else None,
        "address": spot.lots.address if spot.lots else None,
        "pincode": spot.lots.pincode if spot.lots else None,
        "booking_history": [
            {
                "id": h.id,
                "spot_id": h.spot_id,
                "user_id": h.user_id,
                "vehicle_number": h.vehicle_number,
                "start_time": h.start_time.isoformat(),
                "end_time": h.end_time.isoformat() if h.end_time else None,
                "parking_cost": str(h.parking_cost) if h.parking_cost else None,
                "is_paid": h.is_paid
            } for h in history
        ]
    }), 200

@role_required('user')
def release_parking_spot(id):
    booking = BookingHistory.query.get(id)
    if not booking:
        abort(404, description="Booking not found")

    if booking.end_time:
        return jsonify({"msg": "Booking is already ended"}), 400
    
    spot = ParkingSpot.query.get(booking.spot_id)
    if not spot:
        abort(404, description="Parking Spot not found")
    spot.status = 'available'
    db.session.commit()

    if booking:
        booking.end_time = datetime.utcnow()
        booking.parking_cost = (float(spot.lots.price) * ((booking.end_time - booking.start_time).total_seconds() / 3600))
        booking.is_paid = True
        db.session.commit()

    return jsonify({"msg": f"Parking Spot {spot.id} released successfully"}), 200

def get_parking_spot_by_lot_id(lot_id):
    spots = ParkingSpot.query.filter_by(lot_id=lot_id).all()
    if not spots:
        abort(404, description="No parking spots found for this lot")
    
    spots_json = []
    for spot in spots:
        spot_dict = {
            "id": spot.id,
            "status": spot.status
        }
        spots_json.append(spot_dict)

    return jsonify({"spots": spots_json}), 200

@role_required('admin')
def parking_spot_analytics():
    parking_spots = ParkingSpot.query.all()
    analytics = {}
    for spot in parking_spots:
        if spot.status == 'occupied':
            analytics['occupied'] = analytics.get('occupied', 0) + 1
        elif spot.status == 'available':
            analytics['available'] = analytics.get('available', 0) + 1
    return jsonify(data=analytics), 200