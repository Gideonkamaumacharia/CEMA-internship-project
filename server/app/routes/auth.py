# app/routes/auth.py
from flask import Blueprint, jsonify, request
from app.utils.auth import api_key_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/validate', methods=['GET'])
@api_key_required
def validate_api_key():
    # If we got here, the decorator has already ensured the key is valid
    return jsonify({
        "msg":    "API key is valid",
        "doctor": request.doctor.name
    }), 200
