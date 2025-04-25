from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.utils.auth import api_key_required

from app import db
from app.models import HealthProgram

programs_bp = Blueprint('programs', __name__)

@programs_bp.route('/', methods=['POST'])
@api_key_required
def create_program():
    doc_id = get_jwt_identity()
    data = request.get_json() or {}
    name = data.get('name')
    desc = data.get('description', '')

    if not name:
        return jsonify({"msg": "Program name is required"}), 400

    program = HealthProgram(name=name, description=desc, created_by_id=doc_id)
    try:
        db.session.add(program)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "Program name already exists"}), 409

    return jsonify({
        "id": program.id,
        "name": program.name,
        "description": program.description,
        "created_at": program.created_at.isoformat()
    }), 201


@programs_bp.route('/', methods=['GET'])
@api_key_required
def list_programs():
    programs = HealthProgram.query.all()
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "created_at": p.created_at.isoformat()
    } for p in programs]
    return jsonify(result), 200
