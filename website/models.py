from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150))
    lastname = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    #Relaties
    data = db.relationship('Data')
    feedback = db.relationship('Feedback')

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    luchttemp = db.Column(db.Integer)
    opptemp = db.Column(db.Integer)
    # luchtdruk?
    # luchtvochtigheid?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    feedback = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

