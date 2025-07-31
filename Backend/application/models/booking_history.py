from application.database import db
from datetime import datetime

class BookingHistory(db.Model):
    _tablename__ = 'booking_history'

    id = db.Column(db.Integer,primary_key=True)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    vehicle_number = db.Column(db.String(20), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    parking_cost = db.Column(db.Numeric(10,2))
    is_paid = db.Column(db.Boolean, default=False)