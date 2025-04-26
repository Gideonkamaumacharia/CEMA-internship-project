# app/routes/auth.py
from flask import Blueprint, jsonify, request
from app.utils.auth import api_key_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/validate', methods=['GET'])
@api_key_required
def validate_api_key():
    doctor = request.doctor
    
    return jsonify({
            "doctor": {
                "id": doctor.id,
                "name": doctor.name,
                "email": doctor.email,
                "is_admin": doctor.is_admin
            }
        }), 200
