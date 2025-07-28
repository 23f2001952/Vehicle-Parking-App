from application.database import db
from datetime import datetime


class ParkingSpot(db.Model):
    _tablename__ = 'parking_spot'
    id= db.Column(db.Integer, primary_key=True)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'),nullable=False)
    status =  db.Column(db.Enum('available', 'occupied', name='parking_spot_status'),nullable=False,default='available')
