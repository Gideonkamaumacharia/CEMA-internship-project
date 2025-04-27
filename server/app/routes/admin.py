"""
Admin routes for managing doctors and provisioning API keys.

This module allows a super admin to create a new doctor,
generate an API key for them, and send it via email.

"""

from flask import Blueprint, request, jsonify
from flask_mail import Message
import secrets

from app import db, mail
from app.models import Doctor, APIKey
from app.utils.auth import super_admin_required

# Create a Blueprint for admin-related routes
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/doctors', methods=['POST'])
@super_admin_required
def create_and_provision_doctor():
    """
    Create a new doctor and provision an API key.

    This route can only be accessed by a super admin.
    It performs the following steps:
        1. Create a Doctor record.
        2. Revoke any of the doctor's previous API keys (if any).
        3. Generate a new API key and store it.
        4. Send the API key to the doctor's email.
        5. Return a success message.

    Request Body (JSON):
    {
        "name": "Doctor Name",
        "email": "doctor@example.com",
        "is_admin": true
    }

    Returns:
        JSON: Success message.
    """
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    is_admin = data.get('is_admin', False)

    if not (name and email):
        return jsonify({"msg": "Both name and email are required"}), 400

    # Step 1: Create the doctor record
    doctor = Doctor(name=name, email=email, is_admin=is_admin)
    db.session.add(doctor)
    db.session.commit()

    # Step 2: Revoke all their previous API keys (if any exist)
    for key in doctor.api_keys:
        key.is_active = False

    # Step 3: Generate & store a new API key
    new_key = secrets.token_hex(32)
    api_key = APIKey(key=new_key, doctor=doctor)
    db.session.add(api_key)
    db.session.commit()

    # Step 4: Email the new API key to the doctor
    msg = Message(
        subject="Your CEMA Health System API Key",
        recipients=[email],
        body=(
            f"Hello {name},\n\n"
            f"Welcome to CEMA Health System!\n\n"
            f"Your API key is:\n\n    {new_key}\n\n"
            "Please keep it secret, and use it as API-KEY in your requests."
        )
    )
    mail.send(msg)

    # Step 5: Return success response
    return jsonify({"msg": "Doctor created & API key emailed"}), 200
