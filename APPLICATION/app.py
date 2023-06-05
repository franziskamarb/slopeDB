from flask import Flask, url_for, render_template, session, redirect, make_response, jsonify, request
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
from models import Student, Accomodation, Ski, Helmet, Pole, Course, Area, CourseStudent, Shuttle

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
        s_id = 's' + str(random.randint(10000, 99999))

        student = Student(
            student_id=s_id,
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
        session['name'] = form.first_name.data + ' ' + form.last_name.data
        return redirect(url_for('students'))
    form.update_choices()
    return render_template('add_student.html', form=form)


@app.route('/delete_student/<string:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get(student_id)
    if student:
        CourseStudent.query.filter_by(student_student_id=student_id).delete()

        db.session.delete(student)
        db.session.commit()
    return redirect('/students')


@app.route('/courses', methods=['GET'])
def courses():
    course_beginner = Course.query.filter(Course.course_level == "beginner").all()
    course_advanced = Course.query.filter(Course.course_level == "advanced").all()
    course_expert = Course.query.filter(Course.course_level == "expert").all()
    course_students = CourseStudent.query.all()
    students = Student.query.all()
    shuttles = Shuttle.query.all()
    areas = Area.query.all()

    return render_template('courses.html', shuttles=shuttles, students=students, course_students=course_students, course_beginner=course_beginner, course_advanced=course_advanced, course_expert=course_expert, areas=areas)


@app.route('/add_student_to_course', methods=['GET', 'POST'])
def add_student_to_course():
    form = AddStudentCourse()
    if form.validate_on_submit():

        course_studnet = CourseStudent(
            course_course_id=form.course_id.data,
            student_student_id=form.student_id.data
        )
        db.session.add(course_studnet)
        db.session.commit()
        session['known'] = False
        session['name'] = form.course_id.data
        return redirect(url_for('courses'))

    return render_template('add_student_to_course.html', form=form)

@app.route('/del_student_course/<string:student_id>/<string:course_id>', methods=['POST'])
def delete_student_course(student_id, course_id):
    course_student = CourseStudent.query.filter_by(student_student_id=student_id, course_course_id=course_id).first()
    if course_student:
        db.session.delete(course_student)
        db.session.commit()
    return redirect('/courses')

@app.route('/edit_student/<string:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get(student_id)
    form = EditStudentForm(obj=student)
    if form.validate_on_submit():
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.birthdate = form.birthdate.data.strftime('%Y-%m-%d')
        student.adult = calculate_adult(form.birthdate.data)
        student.course_type = form.course_type.data
        student.experience_level = form.experience_level.data
        student.phonenumber = form.phonenumber.data
        student.sex = form.sex.data
        student.street = form.street.data
        student.house_num = form.house_num.data
        student.city = form.city.data
        student.country = form.country.data
        student.post_code = form.post_code.data
        student.accomodation = form.accomodation.data
        student.ski_id = form.ski_id.data
        student.helmet_id = form.helmet_id.data
        student.pole_id = form.pole_id.data
        student.arrival_date = form.arrival_date.data.strftime('%Y-%m-%d')
        student.departure_date = form.departure_date.data.strftime('%Y-%m-%d')
        
        db.session.commit()
        return redirect(url_for('students'))
    
    form.update_choices()
    return render_template('edit_student.html', form=form)


# Forms
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

    ski_id = SelectField('Ski', choices=[], validators=[DataRequired()])
    helmet_id = SelectField('Helmet', choices=[], validators=[DataRequired()])
    pole_id = SelectField('Poles', choices=[], validators=[DataRequired()])

    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddStudentForm, self).__init__(*args, **kwargs)
        self.update_choices() 

    def update_choices(self):
        subquery = db.session.query(Student.ski_id).filter(Student.ski_id.isnot(None)).subquery()
        self.ski_id.choices = [
            (ski.ski_id, f"({ski.ski_id}) {ski.brand} - {ski.modell} - Length: {ski.length}")
            for ski in Ski.query.filter(~Ski.ski_id.in_(subquery)).all()
        ]

        subquery = db.session.query(Student.helmet_id).filter(Student.helmet_id.isnot(None)).subquery()
        self.helmet_id.choices = [
            (helmet.helmet_id, f"({helmet.helmet_id}) {helmet.brand} - Size: {helmet.size}")
            for helmet in Helmet.query.filter(~Helmet.helmet_id.in_(subquery)).all()
        ]

        subquery = db.session.query(Student.pole_id).filter(Student.pole_id.isnot(None)).subquery()
        self.pole_id.choices = [
            (poles.poles_id, f"({poles.poles_id}) {poles.brand} - Length: {poles.length}")
            for poles in Pole.query.filter(~Pole.poles_id.in_(subquery)).all()
        ]


class AddStudentCourse(FlaskForm):
    course_id = SelectField('Course', choices=[], validators=[DataRequired()])
    student_id = SelectField('Student', choices=[], validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(AddStudentCourse, self).__init__(*args, **kwargs)
        self.update_choices() 

    def update_choices(self):
        self.student_id.choices = [
            (student.student_id, f"({student.student_id}) {student.first_name} {student.last_name}")
            for student in Student.query.all()
        ]

        self.course_id.choices = [
            (course.course_id, f"({course.course_id}) {course.course_id} | {course.start_date} - {course.end_date}")
            for course in Course.query.all()
        ]


class EditStudentForm(FlaskForm):
    student_id = StringField('Student ID', render_kw={'disabled': True})
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
    accomodation = SelectField('Accomodation', 
                               choices = 
                               [
                                   (accomodation.accomodation_id, f"{accomodation.name} - {accomodation.city}") 
                                    for accomodation in Accomodation.query.all()
                                ], 
                                validators=[DataRequired()])
    ski_id = SelectField('Ski', choices=[], validators=[DataRequired()])
    helmet_id = SelectField('Helmet', choices=[], validators=[DataRequired()])
    pole_id = SelectField('Poles', choices=[], validators=[DataRequired()])
    arrival_date = DateField('Arrival', validators=[DataRequired()])
    departure_date = DateField('Departure', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(EditStudentForm, self).__init__(*args, **kwargs)
        self.update_choices()


    def update_choices(self):
        student_id = self.student_id.data

        subquery = db.session.query(Student.ski_id).filter(Student.ski_id.isnot(None))
        self.ski_id.choices = [
            (ski.ski_id, f"({ski.ski_id}) {ski.brand} - {ski.modell} - Length: {ski.length}")
            for ski in Ski.query.filter(
                Ski.ski_id.notin_(subquery)
            ).union(
                Ski.query.filter_by(ski_id=Student.query.get(student_id).ski_id)
            ).order_by(Ski.ski_id).all()
        ]

        subquery = db.session.query(Student.helmet_id).filter(Student.helmet_id.isnot(None))
        self.helmet_id.choices = [
            (helmet.helmet_id, f"({helmet.helmet_id}) {helmet.brand} - Size: {helmet.size}")
            for helmet in Helmet.query.filter(
                Helmet.helmet_id.notin_(subquery)
            ).union(
                Helmet.query.filter_by(helmet_id=Student.query.get(student_id).helmet_id)
            ).order_by(Helmet.helmet_id).all()
        ]

        subquery = db.session.query(Student.pole_id).filter(Student.pole_id.isnot(None))
        self.pole_id.choices = [
            (pole.poles_id, f"({pole.poles_id}) {pole.brand} - Length: {pole.length}")
            for pole in Pole.query.filter(
                Pole.poles_id.notin_(subquery)
            ).union(
                Pole.query.filter_by(poles_id=Student.query.get(student_id).pole_id)
            ).order_by(Pole.poles_id).all()
        ]


        

#Other Functions
def calculate_adult(birthdate):
    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    return age >= 18