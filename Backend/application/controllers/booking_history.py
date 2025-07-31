from flask import jsonify, request, abort
from application.models import BookingHistory, User,ParkingLot
from application.database import db
from flask_jwt_extended import jwt_required, current_user
from application.middlewares import role_required


@jwt_required()
def get_booking_history_by_user():
    history = BookingHistory.query.filter_by(user_id=current_user.id).all()
    if not history:
        return jsonify({"msg": "No booking history found"}), 404
    history_json = []
    for booking in history:
        booking_json = {
            "id": booking.id,
            "spot_id": booking.spot_id,
            "user_id": booking.user_id,
            "vehicle_number": booking.vehicle_number,
            "start_time": booking.start_time.isoformat(),
            "end_time": booking.end_time.isoformat() if booking.end_time else None,
            "parking_cost": str(booking.parking_cost) if booking.parking_cost else None,
            "is_paid": booking.is_paid,
            "location": booking.spot.lots.prime_location_name if booking.spot and booking.spot.lots else None
        }
        history_json.append(booking_json)
    return jsonify(data=history_json), 200

@role_required('admin')
def get_booking_history_all():
    history = BookingHistory.query.all()
    if not history:
        return jsonify({"msg": "No booking history found"}), 404
    history_json = []
    for booking in history:
        booking_json = {
            "id": booking.id,
            "spot_id": booking.spot_id,
            "user_id": booking.user_id,
            "vehicle_number": booking.vehicle_number,
            "start_time": booking.start_time.isoformat(),
            "end_time": booking.end_time.isoformat() if booking.end_time else None,
            "parking_cost": str(booking.parking_cost) if booking.parking_cost else None,
            "is_paid": booking.is_paid,
            "location": booking.spot.lots.prime_location_name if booking.spot and booking.spot.lots else None
        }
        history_json.append(booking_json)
    return jsonify(data=history_json), 200

@role_required('admin')
def get_booking_analytics_per_parking_lot():
    parkingLots = ParkingLot.query.all()
    analytics = []
    for lot in parkingLots:
        spots = lot.spots
        for spot in spots:
            bookings = BookingHistory.query.filter_by(spot_id=spot.id).all()
            if bookings:
                for booking in bookings:
                    analytics.append({
                        "spot_id": spot.id,
                        "lot_id": lot.id,
                        "parking_cost": str(booking.parking_cost) if booking.parking_cost else None,
                        "is_paid": booking.is_paid
                    })
    if not analytics:
        return jsonify({"msg": "No booking analytics found"}), 404
    return jsonify(data=analytics), 200
