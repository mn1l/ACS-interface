from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    feedback = db.Column(db.Integer, db.CheckConstraint('feedback > 0 AND feedback < 5')) # weet niet of dit werkt?
    data = db.relationship('Data')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    luchttemp = db.Column(db.Integer)
    opptemp = db.Column(db.Integer)
    # luchtdruk?
    # luchtvochtigheid?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))