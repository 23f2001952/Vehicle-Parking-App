from application.database import db
from .booking_history import BookingHistory

class User(db.Model):
    _tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.Text, unique=True, nullable = False)
    email = db.Column(db.Text, unique=True, nullable = False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.Text, nullable=False, default='user')
    blocked = db.Column(db.Boolean , nullable = False, default = False)
    address = db.Column(db.Text)
    pincode = db.Column(db.String(6))
    bookinghistory = db.relationship('BookingHistory',backref='user',lazy=True)