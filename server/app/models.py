from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from . import db
from flask_sqlalchemy import SQLAlchemy

#db = SQLAlchemy()

class Doctor(db.Model):
    __tablename__ = 'doctors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    

    # relationships
    clients = db.relationship('Client', back_populates='created_by')
    programs = db.relationship('HealthProgram', back_populates='created_by')
    api_keys  = db.relationship('APIKey', back_populates='doctor',
                                 cascade='all, delete-orphan')

class APIKey(db.Model):
    __tablename__ = 'api_keys'
    id         = db.Column(db.Integer, primary_key=True)
    key        = db.Column(db.String(64), unique=True, nullable=False, index=True)
    doctor_id  = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_active  = db.Column(db.Boolean, default=True, nullable=False)

    doctor = db.relationship('Doctor', back_populates='api_keys')
    

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    contact_info = db.Column(db.Text, nullable=True)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    created_by = db.relationship('Doctor', back_populates='clients')

    # association to Enrollment
    enrollments = db.relationship('Enrollment', back_populates='client', cascade='all, delete-orphan', overlaps='programs,clients')
    # convenience: directly list programs
    programs = db.relationship(
        'HealthProgram',
        secondary='enrollments',
        back_populates='clients',
        overlaps='enrollments'
    )


class HealthProgram(db.Model):
    __tablename__ = 'health_programs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    created_by_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    created_by = db.relationship('Doctor', back_populates='programs')

    enrollments = db.relationship('Enrollment', back_populates='program', cascade='all, delete-orphan',overlaps='clients,programs')
    clients = db.relationship(
        'Client',
        secondary='enrollments',
        back_populates='programs',
        overlaps='enrollments'
    )


class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    program_id = db.Column(db.Integer, db.ForeignKey('health_programs.id'), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(50), default='active')  # e.g. active, completed, dropped

    client = db.relationship('Client', back_populates='enrollments',overlaps='programs,clients')
    program = db.relationship('HealthProgram', back_populates='enrollments',overlaps='clients,programs')
