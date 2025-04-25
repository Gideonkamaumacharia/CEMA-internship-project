from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app import db
from app.models import Client, HealthProgram, Enrollment
from app.utils.auth import api_key_required

enroll_bp = Blueprint('enrollments', __name__)

@enroll_bp.route('/<int:client_id>', methods=['POST'])
@api_key_required
def enroll_client(client_id):
    data = request.get_json() or {}
    ids = data.get('program_ids', [])
    if not ids or not isinstance(ids, list):
        return jsonify({"msg": "program_ids must be a list of IDs"}), 400

    client = Client.query.get_or_404(client_id)
    enrollments = []

    for pid in ids:
        prog = HealthProgram.query.get(pid)
        if not prog:
            continue
        existing = Enrollment.query.filter_by(client_id=client.id, program_id=pid).first()
        if existing:
            continue
        e = Enrollment(client=client, program=prog)
        db.session.add(e)
        enrollments.append(e)

    db.session.commit()
    return jsonify([{
        "client_id": e.client_id,
        "program_id": e.program_id,
        "enrolled_at": e.enrolled_at.isoformat(),
        "status": e.status
    } for e in enrollments]), 201
