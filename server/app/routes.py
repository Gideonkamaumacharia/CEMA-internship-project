from flask import Blueprint,jsonify,request,current_app,send_from_directory
from .models import  Doctor, Client, HealthProgram, Enrollment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import bcrypt,db
import re

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return jsonify({'message':'Welcome to the Health Management System API'}), 200

def validate_email(email):
    return re.match(r'^[^@]+@[^@]+\.[^@]+$', email)

def validate_password(password):
    return re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$', password)


@main_bp.route('/auth/register', methods=['POST'])
def register_doctor():
    """
    Register a new doctor account.
    Request JSON: { "name": str, "email": str, "password": str }
    Returns: { "msg": "...", "doctor": {...} }
    """
    data = request.get_json()

    required_fields = ["name", "email", "password"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400
        
    name = data['name']
    email = data['email']
    password = data['password']

    if not validate_email(data['email']):
        return jsonify({'message': 'Invalid email format'}), 400
    
    if not validate_password(data['password']):
        return jsonify({'message': 'Password must be at least 8 characters long, contain at least one uppercase letter, one number, and one special character.'}), 400
    
    
    
    user_email = Doctor.query.filter_by(email=data['email']).first()
    if user_email:
        return jsonify({'message': 'Email already exists'}),409

    
    password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    doctor = Doctor(name=name, email=email, password=password)
    try:
        db.session.add(doctor)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Email already registered"}), 409

    return jsonify({
        "msg": "Doctor registered",
        "doctor": {"id": doctor.id, "name": doctor.name, "email": doctor.email}
    }), 200
