from flask import Flask, url_for, render_template, session, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os

app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@database:5432/slopeDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Test(db.Model):
    __tablename__ = 'test'

    test_id = db.Column(db.String(64), primary_key = True)
    name = db.Column(db.String(100))

    def json(self):
        return {'test_id': test_id, 'name': name}
    
app.app_context().push()
db.create_all()

@app.route('/test')
def index():
    return f"{Test.query.all()}"