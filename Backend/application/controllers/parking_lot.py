from application.models import ParkingLot , ParkingSpot,BookingHistory
from application.middlewares import role_required
from flask_jwt_extended import jwt_required
from application.database import db
from flask import jsonify,request,abort


@role_required('admin')
def add_parking_lot():

    prime_location_name = request.json.get("prime_location_name",None)
    price = request.json.get("price",None)
    address =request.json.get("address",None)
    number_of_spots = request.json.get("number_of_spots",None)
    pincode = request.json.get("pincode",None)



    if not prime_location_name or not price or not address or not number_of_spots or not pincode:
        return jsonify({
            "msg" : "Please enter all the required fields"
        })
    
    new_lot = ParkingLot(prime_location_name=prime_location_name,price=price,address=address,number_of_spots=number_of_spots,pincode=pincode)
    db.session.add(new_lot)
    db.session.flush()
    for i in range(number_of_spots):
        db.session.add(ParkingSpot(lot_id=new_lot.id))
    db.session.commit()

    return jsonify({
        "msg" : "Parking Lot Successfuly Created"
    }),201
    

@jwt_required()
def get_all_parking_lot():
    parking_lots = ParkingLot.query.all()
    parking_lots_json = []
    for lot in parking_lots:
        parking_lot = {}
        parking_lot["id"] = lot.id
        parking_lot["prime_location_name"] = lot.prime_location_name
        parking_lot["price"] = lot.price
        parking_lot["address"] = lot.address
        parking_lot["number_of_spots"] = lot.number_of_spots
        parking_lot["pincode"] = lot.pincode
        parking_lots_json.append(parking_lot)

    return jsonify({"ParkingLots":parking_lots_json})

@role_required('admin')
def delete_parking_lot(id):
    parking_lot = ParkingLot.query.get(id)
    if not parking_lot:
        abort(404, description="ParkingLot not found")

    spots = parking_lot.spots

    for spot in spots:
        if spot.status == 'occupied':
            return  abort(400, description="Cannot delete lot. Some spots are still occupied.")
        
    for spot in parking_lot.spots:
        db.session.delete(spot)

    db.session.delete(parking_lot)
    db.session.commit()

    return  jsonify({
        "msg": f"Parking lot with ID {id} deleted successfully."
    }), 200

@jwt_required()
def get_parking_lot_by_id(id):  
    parking_lot = ParkingLot.query.get(id)

    if not parking_lot:
        abort(404, description="Parking lot not found.")

    spots = parking_lot.spots

    spots_json=[]
    
    for spot in spots:
        spot_dict = {}
        spot_dict["id"]  = spot.id
        spot_dict["status"] = spot.status

        spots_json.append(spot_dict)
        

    return jsonify(
        {
            "prime_location_name": parking_lot.prime_location_name,
            "price" : parking_lot.price,
            "address" : parking_lot.address,
            "number_of_spots" : parking_lot.number_of_spots,
            "pincode" : parking_lot.pincode,
            "spots" : spots_json
        }
    ), 200

@role_required('admin')
def update_parking_lot(id):
    parking_lot = ParkingLot.query.get(id)

    
    if not parking_lot:
        abort(404, description="Parking lot not found.")
    previous_spots = parking_lot.number_of_spots
    prime_location_name = request.json.get("prime_location_name", None)
    price = request.json.get("price", None)
    address = request.json.get("address", None)
    number_of_spots = request.json.get("number_of_spots", None)
    pincode = request.json.get("pincode", None)

    if not prime_location_name or not price or not address or not number_of_spots or not pincode:
        return jsonify({
            "msg": "Please enter all the required fields"
        }), 400
    parking_lot.prime_location_name = prime_location_name
    parking_lot.price = price
    parking_lot.address = address
    parking_lot.pincode = pincode
    if number_of_spots < previous_spots:
        spots_to_remove = previous_spots - number_of_spots
        available_spots = ParkingSpot.query.filter_by(lot_id=parking_lot.id, status='available').all()
        if len(available_spots) < spots_to_remove:
            return jsonify({
                "msg": "Not enough available spots to remove."
            }), 400
        for spot in available_spots[:spots_to_remove]:
            db.session.delete(spot)
    elif number_of_spots > previous_spots:
        spots_to_add = number_of_spots - previous_spots
        for _ in range(spots_to_add):
            new_spot = ParkingSpot(lot_id=parking_lot.id)
            db.session.add(new_spot)
    parking_lot.number_of_spots = number_of_spots
    db.session.commit()
    return jsonify({
        "msg": "Parking lot updated successfully."
    }), 200

def get_available_spots_by_lot_id(lot_id):
    parking_lot = ParkingLot.query.get(lot_id)
    if not parking_lot:
        abort(404, description="Parking lot not found.")
    
    available_spots = ParkingSpot.query.filter_by(lot_id=lot_id, status='available').all()
    if not available_spots:
        return jsonify({"msg": "No available spots found"}), 404
    
    available_spots_json = []
    for spot in available_spots:
        available_spots_json.append({
            "id": spot.id,
            "lot_id": spot.lot_id,
            "status": spot.status
        })
    
    return jsonify({"AvailableSpots": available_spots_json}), 200

@role_required('admin')
def get_parking_lot_analytics():
    parking_lots = ParkingLot.query.all()
    analytics = {}

    for lot in parking_lots:
        total_spots = lot.number_of_spots
        available_spots = ParkingSpot.query.filter_by(lot_id=lot.id, status='available').count()
        occupied_spots = total_spots - available_spots

        analytics[lot.id] = {
            "total_spots": total_spots,
            "available_spots": available_spots,
            "occupied_spots": occupied_spots
        }

    if not analytics:
        return jsonify({"msg": "No parking lot analytics found"}), 404

    return jsonify(data=analytics), 200