from flask import Blueprint, jsonify, request
from app import db
from app.models import Client, HealthProgram, Enrollment
from app.utils.auth import api_key_required

# Blueprint for handling client enrollments in health programs
enroll_bp = Blueprint('enrollments', __name__)

@enroll_bp.route('/<int:client_id>', methods=['POST'])
@api_key_required
def enroll_client(client_id):
    """
    Enroll a client in one or more health programs.

    Args:
        client_id (int): The ID of the client to enroll.
    
    Request body should include:
        - program_ids (list): A list of health program IDs to enroll the client in.

    Returns:
        JSON response indicating success or failure.
    """
    # Get the data from the request (assumed to be in JSON format)
    data = request.get_json() or {}
    
    # Extract the list of program IDs to enroll the client in
    program_ids = data.get('program_ids', [])

    # Ensure program_ids is a list and contains at least one program ID
    if not program_ids or not isinstance(program_ids, list):
        return jsonify({"msg": "program_ids must be a list of IDs"}), 400

    # Retrieve the client by their client_id, return 404 if not found
    client = Client.query.get_or_404(client_id)

    # Initialize a list to hold the new enrollment objects
    enrollments = []

    # Process each program ID to enroll the client
    for program_id in program_ids:
        # Find the program corresponding to the current ID
        program = HealthProgram.query.get(program_id)
        if not program:
            # If the program doesn't exist, skip to the next one
            continue
        
        # Check if the client is already enrolled in the program
        existing = Enrollment.query.filter_by(client_id=client.id, program_id=program_id).first()
        if existing:
            # If already enrolled, skip to the next program
            continue
        
        # Create a new enrollment record
        enrollment = Enrollment(client=client, program=program)
        
        # Add the new enrollment to the session for later commit
        db.session.add(enrollment)
        enrollments.append(enrollment)

    # Commit the changes to the database
    db.session.commit()

    # Return a success message indicating that the client was enrolled
    return jsonify({
        "message": "Client enrolled successfully"
    }), 200
