from application.models import ParkingLot , ParkingSpot
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
def update_parking_lot():
    return