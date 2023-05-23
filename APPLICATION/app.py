from flask import Flask, url_for, render_template, session, redirect, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
import os
from sqlalchemy.ext.automap import automap_base

app = Flask (__name__)
bootstrap = Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:1234@database:5432/slopeDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hard to guess string'

db = SQLAlchemy(app)

from models import Student, Accomodation, Ski

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
        student = Student(
            student_id="test_id",
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            birthdate="2005-05-21",
            adult=True,
            course_type="",
            experience_level="",
            phonenumber="",
            sex="",
            street="",
            house_num="",
            city="",
            country="",
            post_code=11111,
            accomodation="A1",
            ski_id="SM60",
            helmet_id="H60",
            pole_id="P60",
            arrival_date="2005-05-21",
            departure_date="2005-05-21"
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
    birthdate = StringField('Birthdate', validators=[DataRequired()])
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
    ski = SelectField('Ski',
                      choices = 
                      [
                          (ski.ski_id, f"({ski.ski_id}) {ski.brand} - {ski.modell} - Size: {ski.length}")
                           for ski in Ski.query.filter(~Ski.ski_id.in_(subquery)).all()
                        ], 
                        validators=[DataRequired()])
    
    submit = SubmitField('Submit')