from flask import Flask, url_for, render_template, session, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from sqlalchemy.ext.automap import automap_base

app = Flask (__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@database:5432/slopeDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from models import accomodation

app.app_context().push()
db.create_all()

@app.route('/')
def index():
    title="List of employees:"
    employees = accomodation.query.order_by(accomodation.name.desc()).all()
    return render_template('accomodations.html', employees=employees)


#@app.route('/test')
#def index():
#    return f"results: {len(accomodation.query.order_by(accomodation.name).all())}"