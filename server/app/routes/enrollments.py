from flask import Blueprint, jsonify, request
from app import db
from app.models import Client, HealthProgram, Enrollment
from app.utils.auth import api_key_required

enroll_bp = Blueprint('enrollments', __name__)

@enroll_bp.route('/<int:client_id>', methods=['POST'])
@api_key_required
def enroll_client(client_id):
    data = request.get_json() or {}
    program_ids = data.get('program_ids', [])
    if not program_ids or not isinstance(program_ids, list):
        return jsonify({"msg": "program_ids must be a list of IDs"}), 400

    client = Client.query.get_or_404(client_id)
    enrollments = []

    for program_id in program_ids:
        program = HealthProgram.query.get(program_id)
        if not program:
            continue
        existing = Enrollment.query.filter_by(client_id=client.id, program_id=program_id).first()
        if existing:
            continue
        enrollment = Enrollment(client=client, program=program)
        db.session.add(enrollment)
        enrollments.append(enrollment)

    db.session.commit()
    return jsonify([{
        "client_id": enrollment.client_id,
        "program_id": enrollment.program_id,
        "program_name": enrollment.program.name,
        "enrolled_at": enrollment.enrolled_at.isoformat(),
        "status": enrollment.status
    } for enrollment in enrollments]), 201
