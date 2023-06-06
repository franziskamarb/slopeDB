from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from app import db

class Salary(db.Model):
    __tablename__ = 'salary'

    salary_group = db.Column(db.String, primary_key=True)
    salary = db.Column(db.BigInteger)


class Employee(db.Model):
    __tablename__ = 'employee'

    employee_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    job_title = db.Column(db.String)
    salary_group = db.Column(db.String, db.ForeignKey('salary.salary_group'))
    instructor_level = db.Column(db.String)
    street = db.Column(db.String)
    house_num = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    post_code = db.Column(db.String)
    birthdate = db.Column(db.Date)
    age = db.Column(db.BigInteger)
    sex = db.Column(db.String)
    phonenumber = db.Column(db.String)
    salary = db.relationship('Salary')


class Accomodation(db.Model):
    __tablename__ = 'accomodation'

    accomodation_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)
    street = db.Column(db.String)
    house_num = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    post_code = db.Column(db.String)


class Ski(db.Model):
    __tablename__ = 'ski'

    ski_id = db.Column(db.String, primary_key=True)
    modell = db.Column(db.String)
    brand = db.Column(db.String)
    length = db.Column(db.String)


class Helmet(db.Model):
    __tablename__ = 'helmets'

    helmet_id = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String)
    size = db.Column(db.String)


class Pole(db.Model):
    __tablename__ = 'poles'

    poles_id = db.Column(db.String, primary_key=True)
    brand = db.Column(db.String)
    length = db.Column(db.String)


class Student(db.Model):
    __tablename__ = 'student'

    student_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthdate = db.Column(db.Date)
    adult = db.Column(db.Boolean)
    course_type = db.Column(db.String)
    experience_level = db.Column(db.String)
    phonenumber = db.Column(db.String)
    sex = db.Column(db.String)
    street = db.Column(db.String)
    house_num = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    post_code = db.Column(db.BigInteger)
    accomodation = db.Column(db.String, db.ForeignKey('accomodation.accomodation_id'))
    ski_id = db.Column(db.String, db.ForeignKey('ski.ski_id'), unique=True)
    helmet_id = db.Column(db.String, db.ForeignKey('helmets.helmet_id'), unique=True)
    pole_id = db.Column(db.String, db.ForeignKey('poles.poles_id'), unique=True)
    arrival_date = db.Column(db.Date)
    departure_date = db.Column(db.Date)
    accomodation_obj = db.relationship('Accomodation')
    ski = db.relationship('Ski')
    helmet = db.relationship('Helmet')
    pole = db.relationship('Pole')


class Area(db.Model):
    __tablename__ = 'area'

    area_id = db.Column(db.String, primary_key=True)
    country = db.Column(db.String)
    city = db.Column(db.String)
    name = db.Column(db.String)
    difficulty_level = db.Column(db.String)
    openting_time = db.Column(db.Time)
    closing_time = db.Column(db.Time)
    magic_carpet = db.Column(db.Boolean)


class Shuttle(db.Model):
    __tablename__ = 'shuttle'

    shuttle_name = db.Column(db.String, primary_key=True)
    type = db.Column(db.String)
    start_location = db.Column(db.String)
    end_location = db.Column(db.String)
    capacity = db.Column(db.BigInteger)
    area_id = db.Column(db.String, db.ForeignKey('area.area_id'))
    area = db.relationship('Area')


class Course(db.Model):
    __tablename__ = 'course'

    course_id = db.Column(db.String, primary_key=True)
    course_level = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    area = db.Column(db.String, db.ForeignKey('area.area_id'))
    employee_id = db.Column(db.String, db.ForeignKey('employee.employee_id'))
    area_obj = db.relationship('Area')
    employee = db.relationship('Employee')


class CourseStudent(db.Model):
    __tablename__ = 'course_student'

    course_course_id = db.Column(db.String, db.ForeignKey('course.course_id'), primary_key=True)
    student_student_id = db.Column(db.String, db.ForeignKey('student.student_id'), primary_key=True)
    course = db.relationship('Course')
    student = db.relationship('Student')


class EmployeeView(db.Model):
    __tablename__ = 'v_employee'

    employee_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    job_title = db.Column(db.String)
    salary_group = db.Column(db.String)
    salary = db.Column(db.Float)
    instructor_level = db.Column(db.String)
    street = db.Column(db.String)
    house_num = db.Column(db.String)
    city = db.Column(db.String)
    country = db.Column(db.String)
    post_code = db.Column(db.String)
    birthdate = db.Column(db.Date)
    age = db.Column(db.Integer)
    sex = db.Column(db.String)
    phonenumber = db.Column(db.String)