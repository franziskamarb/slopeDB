from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from app import db



class ACCOMODATION(db.Model):
    __tablename__ = 'ACCOMODATION'
    accomodation_id = db.Column('accomodation_id', db.String(64), primary_key = True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    street = db.Column(db.String(100))
    house_num = db.Column(db.String(100))
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    post_code = db.Column(db.String(100))