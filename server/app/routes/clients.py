from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from sqlalchemy import or_
from app.utils.auth import api_key_required


from app import db
from app.models import Client

clients_bp = Blueprint('clients', __name__)

@clients_bp.route('/register', methods=['POST'])
@api_key_required
def register_client():
    doctor = request.doctor

    doctor_id = doctor.id
    data = request.get_json() or {}
    try:
        dob = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None
    except ValueError:
        return jsonify({"msg": "Invalid date_of_birth format"}), 400

    client = Client(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=dob,
        gender=data.get('gender'),
        contact_info=data.get('contact_info'),
        created_by_id=doctor_id
    )

    if not (client.first_name and client.last_name):
        return jsonify({"msg": "first_name and last_name required"}), 400

    db.session.add(client)
    db.session.commit()
    return jsonify({
        "id": client.id,
        "first_name": client.first_name,
        "last_name": client.last_name,
        "registered_at": client.registered_at.isoformat()
    }), 200


@clients_bp.route('/', methods=['GET'])
@api_key_required
def list_clients():
    clients = Client.query.all()
    return jsonify([{ "id": client.id, "first_name": client.first_name, "last_name": client.last_name } for client in clients]), 200


@clients_bp.route('/search', methods=['GET'])
@api_key_required
def search_clients():
    q = request.args.get('q', '').strip()
    if not q:
        return jsonify({"msg": "Query parameter 'q' is required"}), 400

    like = f"%{q}%"
    matches = Client.query.filter(or_(Client.first_name.ilike(like), Client.last_name.ilike(like))).all()

    return jsonify([{ "id": c.id, "first_name": c.first_name, "last_name": c.last_name } for c in matches]), 200


@clients_bp.route('/<int:client_id>', methods=['GET'])
@api_key_required
def get_client_profile(client_id):
    client = Client.query.get_or_404(client_id)
    programs = [{
        "id": e.program.id,
        "name": e.program.name,
        "enrolled_at": e.enrolled_at.isoformat(),
        "status": e.status
    } for e in client.enrollments]

    return jsonify({
        "client": {
            "id": client.id,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "date_of_birth": client.date_of_birth.isoformat() if client.date_of_birth else None,
            "gender": client.gender,
            "contact_info": client.contact_info,
            "registered_at": client.registered_at.isoformat()
        },
        "programs": programs
    }), 200

