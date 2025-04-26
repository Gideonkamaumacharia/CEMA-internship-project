# app/routes/admin.py
from flask import Blueprint, request, jsonify
from app.utils.auth import super_admin_required
from app.models import Doctor, APIKey
from app import db, mail
from flask_mail import Message
import secrets

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/doctors', methods=['POST'])
@super_admin_required
def create_and_provision_doctor():
    data = request.get_json() or {}
    name  = data.get('name')
    email = data.get('email')
    is_admin = data.get('is_admin', False)

    if not (name and email):
        return jsonify({"msg": "Both name and email are required"}), 400

    # 1) Create the doctor record
    doctor = Doctor(name=name, email=email, is_admin=is_admin)
    db.session.add(doctor)
    db.session.commit()

    # 1) Revoke all their previous keys
    for k in doctor.api_keys:
        k.is_active = False

    # 2) Generate & store API key
    new_key = secrets.token_hex(32)
    api_key = APIKey(key=new_key, doctor=doctor)
    db.session.add(api_key)
    db.session.commit()

    # 3) Email the key
    msg = Message(
        subject="Your CEMA Health System API Key",
        recipients=[email],
        body=(
          f"Hello {name},\n\n"
          f"Welcome to CEMA Health System!\n"
          f"Your API key is:\n\n    {new_key}\n\n"
          "Please keep it secret, and use it as API-KEY in your requests."
        )
    )
    mail.send(msg)

    # 4) Return doctor ID
    return jsonify({"doctor_id": doctor.id, "msg": "Doctor created & API key emailed"}), 201
