from application.database import db
from .parking_spot import ParkingSpot

class ParkingLot(db.Model):
    _tablename__ = 'parking_lot'
    id = db.Column(db.Integer, primary_key = True)
    prime_location_name = db.Column(db.Text, nullable = False)
    price = db.Column(db.Numeric(10,2), nullable = False)
    address = db.Column(db.Text, nullable = False)
    number_of_spots = db.Column(db.Integer, nullable= False, default=0)
    pincode = db.Column(db.String(6), nullable = False)
    spots = db.relationship('ParkingSpot',backref='lots', lazy=True)