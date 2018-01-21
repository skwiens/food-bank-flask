# from flask import Flask
from app import db

openhour_volunteers = db.Table('openhour_volunteers',
    db.Column('openhour_id', db.Integer, db.ForeignKey('openhour.id')),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id'))
)

openhour_shoppers = db.Table('openhour_shoppers',
    db.Column('openhour_id', db.Integer, db.ForeignKey('openhour.id')),
    db.Column('volunteer_id', db.Integer, db.ForeignKey('volunteer.id'))
)

class Openhour(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    # author = db.Column(db.Integer(), db.ForeignKey('volunteer.id'))
    # author = db.Column(db.String(255))
    date = db.Column(db.DateTime())
    posted = db.Column(db.Boolean)
    volunteers = db.relationship('Volunteer', secondary=openhour_volunteers, backref='openhourvols', lazy='dynamic')
    shoppers = db.relationship('Volunteer', secondary=openhour_shoppers, backref='openhourshoppers', lazy='dynamic' )
    notes = db.relationship('Note', backref='openhournotes', lazy=True)

    def __init__(self, date):
        self.date = date

    def __repr__(self):
        return "<Openhour '{}'>".format(self.date)

class Volunteer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(50))
    email = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean)
    openhours = db.relationship('Openhour', secondary=openhour_volunteers, backref='ohvolunteers', lazy='subquery')
    openhour_shoppers = db.relationship('Openhour', secondary=openhour_shoppers, backref='ohshoppers', lazy='subquery')
    notes = db.relationship('Note', backref='openhour', lazy=True)


    def __init__(self, name, email, role, active):
        self.name = name
        self.email = email
        self.role = role
        self.active = active

    def __repr__(self):
        return "<Volunteer '{}'>".format(self.name)

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User'{}'>".format(self.username)

class Note(db.Model):
    id=db.Column(db.Integer(), primary_key=True)
    openhour_id = db.Column(db.Integer, db.ForeignKey('openhour.id'), nullable=False)
    author = db.Column(db.Integer(), db.ForeignKey('volunteer.id'))
    customers = db.Column(db.Integer())
    body = db.Column(db.Text())
    shopping = db.Column(db.Text())

class Email(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    send_date = db.Column(db.DateTime())
    recipients = db.Column(db.String(255))
    subject = db.Column(db.String(255))
    message = db.Column(db.Text())
