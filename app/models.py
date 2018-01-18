# from flask import Flask
from app import db

class Openhour(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # author = db.Column(db.Integer(), db.ForeignKey('volunteer.id'))
    # author = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    # volunteers = db.relationship('Volunteer', secondary=openhour_volunteers, backref='openhourvols', lazy='dynamic')
    # shoppers = db.relationship('Volunteer', secondary=openhour_shoppers, backref='openhourshoppers', lazy='dynamic' )
    # notes = db.relationship('Note', backref='openhournotes', lazy=True)
    volunteers = db.Column(db.String(255))
    shoppers = db.Column(db.String(255))
    # customers = db.Column(db.Integer())
    # notes = db.Column(db.Text())
    # shopping = db.Column(db.Text())
