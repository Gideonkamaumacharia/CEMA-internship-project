"""
Authentication routes for API key validation.

This module provides a route to validate an API key
and retrieve associated doctor information.
"""

from flask import Blueprint, jsonify, request
from app.utils.auth import api_key_required

# Create a Blueprint for authentication-related routes
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/validate', methods=['GET'])
@api_key_required
def validate_api_key():
    """
    Validate the provided API key and return doctor details.

    This route is protected and requires a valid API key in the request headers.

    Returns:
        JSON: Doctor information if the API key is valid.
    """
    
    doctor = request.doctor

    return jsonify({
        "doctor": {
            "id": doctor.id,
            "name": doctor.name,
            "email": doctor.email,
            "is_admin": doctor.is_admin
        }
    }), 200
