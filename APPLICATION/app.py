from flask import Flask, url_for, render_template, session, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from sqlalchemy.ext.automap import automap_base
from datetime import datetime, date
import random

app = Flask (__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@database:5432/slopeDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)

from models import Student, Accomodation, Ski, Helmet, Pole

app.app_context().push()
db.create_all()

@app.route('/')
def index():
    title="landing page"
    return render_template('landing_page.html')

@app.route('/students', methods=['GET'])
def students():
    students = Student.query.order_by(Student.last_name.asc()).all()

    return render_template('students.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():

        raw_birthdate = form.birthdate.data
        raw_arrival = form.arrival_date.data
        raw_departure = form.departure_date.data

        student = Student(
            student_id='s' + str(random.randint(10000, 99999)),
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            birthdate = raw_birthdate.strftime('%Y-%m-%d'),
            adult = calculate_adult(raw_birthdate),
            course_type=form.course_type.data,
            experience_level=form.experience_level.data,
            phonenumber=form.phonenumber.data,
            sex=form.sex.data,
            street=form.street.data,
            house_num=form.house_num.data,
            city=form.city.data,
            country=form.country.data,
            post_code=form.post_code.data,
            accomodation=form.accomodation.data,
            ski_id=form.ski_id.data,
            helmet_id=form.helmet_id.data,
            pole_id=form.pole_id.data,
            arrival_date=raw_arrival.strftime('%Y-%m-%d'),
            departure_date=raw_departure.strftime('%Y-%m-%d')
        )
        db.session.add(student)
        db.session.commit()
        session['known'] = False
        session['name'] = form.first_name.data
        return redirect(url_for('index'))

    return render_template('add_student.html', form=form)

#Forms
class AddStudentForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    birthdate = DateField('Birthdate', validators=[DataRequired()])  
    course_type = SelectField('Course Type',
                               choices=[('Ski', 'Ski'), ('Snowboard', 'Snowboard')],
                                 validators=[DataRequired()])
    experience_level = SelectField('Experience Level', 
                                   choices=[('beginner', 'Beginner'), ('advanced', 'Advanced'), ('expert', 'Expert')],
                                   validators=[DataRequired()])
    phonenumber = StringField('Phonenumber', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female')], validators=[DataRequired()])
    street = StringField('Street', validators=[DataRequired()])
    house_num = StringField('House Number', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    post_code = StringField('Post Code', validators=[DataRequired()])
    arrival_date = DateField('Arrival', validators=[DataRequired()])
    departure_date = DateField('Departure', validators=[DataRequired()])  
    accomodation = SelectField('Accomodation', 
                               choices = 
                               [
                                   (accomodation.accomodation_id, f"{accomodation.name} - {accomodation.city}") 
                                    for accomodation in Accomodation.query.all()
                                ], 
                                validators=[DataRequired()])
    subquery = db.session.query(Student.ski_id).subquery()
    ski_id = SelectField('Ski',
                      choices = 
                      [
                          (ski.ski_id, f"({ski.ski_id}) {ski.brand} - {ski.modell} - Length: {ski.length}")
                           for ski in Ski.query.filter(~Ski.ski_id.in_(subquery)).all()
                        ], 
                        validators=[DataRequired()])
    helmet_id = SelectField('Helmet',
                      choices = 
                      [
                          (helmet.helmet_id, f"({helmet.helmet_id}) {helmet.brand} - Size: {helmet.size}")
                           for helmet in Helmet.query.filter(~Helmet.helmet_id.in_(db.session.query(Student.helmet_id).subquery())).all()
                        ], 
                        validators=[DataRequired()])
    pole_id = SelectField('Poles',
                      choices = 
                      [
                          (poles.poles_id, f"({poles.poles_id}) {poles.brand} - Length: {poles.length}")
                           for poles in Pole.query.filter(~Pole.poles_id.in_(db.session.query(Student.pole_id).subquery())).all()
                        ], 
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


#Other Functions
def calculate_adult(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age >= 18
