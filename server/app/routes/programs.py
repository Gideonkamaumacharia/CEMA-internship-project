from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.utils.auth import api_key_required
from app import db
from app.models import HealthProgram

# Blueprint for handling health program-related operations
programs_bp = Blueprint('programs', __name__)

@programs_bp.route('/create', methods=['POST'])
@api_key_required
def create_program():
    """
    Endpoint to create a new health program.

    Request body should include:
        - name (string): Name of the health program.
        - description (string): Description of the health program.

    Returns:
        JSON response indicating success or failure.
    """
    # Get the doctor who is creating the program
    doctor = request.doctor
    doctor_id = doctor.id

    # Extract program data from the request
    data = request.get_json() or {}
    name = data.get('name')
    desc = data.get('description', '')

    # Ensure the required fields are present in the request
    required_fields = ["name", "description"]
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"{field} is required"}), 400

    # Create a new health program instance
    program = HealthProgram(name=name, description=desc, created_by_id=doctor_id)

    try:
        # Add the program to the database session and commit
        db.session.add(program)
        db.session.commit()
    except IntegrityError:
        # Rollback and return an error if the program name already exists
        db.session.rollback()
        return jsonify({"msg": "Program name already exists"}), 409

    # Return a success message indicating the program was created
    return jsonify({
        "message": "Program created successfully"
    }), 200


@programs_bp.route('/list', methods=['GET'])
@api_key_required
def list_programs():
    """
    Endpoint to list all health programs.

    Returns:
        JSON response containing the list of programs.
    """
    # Retrieve all programs from the database
    programs = HealthProgram.query.all()

    # Prepare the list of program data to return
    result = [{
        "id": p.id,
        "name": p.name,
        "description": p.description,
        "created_at": p.created_at.isoformat()  # Format datetime for response
    } for p in programs]

    # Return the list of programs
    return jsonify(result), 200
