# app/utils/auth.py

from functools import wraps
from flask import request, jsonify
from app.models import APIKey

def api_key_required(f):
    """
    Decorator to enforce that a valid, active API key is provided
    in the API-KEY header.  On success, attaches `request.doctor`.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
    
        key = request.headers.get('API-KEY')
        if not key:
            return jsonify({"msg": "API key required"}), 401

        record = APIKey.query.filter_by(key=key, is_active=True).first()
        if not record:
            return jsonify({"msg": "Invalid or revoked API key"}), 403

        # Expose the authenticated Doctor on the request
        request.doctor = record.doctor
        return f(*args, **kwargs)

    return decorated

def super_admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # First validate API key just like a normal decorator
        key = request.headers.get('API-KEY')
        if not key:
            return jsonify({"msg": "API key required"}), 401
        
        record = APIKey.query.filter_by(key=key, is_active=True).first()
        if not record:
            return jsonify({"msg": "Invalid or revoked API key"}), 403

        # Now check the doctor’s “is_admin” flag (or however you mark superadmins)
        doctor = record.doctor
        if not getattr(doctor, 'is_admin', False):
            return jsonify({"msg": "Super-admin privileges required"}), 403

        # Expose the authenticated Doctor on the request
        request.doctor = doctor
        return f(*args, **kwargs)
    return decorated