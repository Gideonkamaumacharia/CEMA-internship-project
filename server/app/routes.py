from flask import Blueprint,jsonify,request,current_app,send_from_directory
from .models import  Doctor, Client, HealthProgram, Enrollment
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import current_app
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from app import bcrypt,db

main_bp = Blueprint('main',__name__)

@main_bp.route('/')
def index():
    return jsonify({'message':'Welcome to the Health Management System API'}), 200