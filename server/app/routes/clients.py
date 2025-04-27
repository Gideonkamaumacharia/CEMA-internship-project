from flask import Blueprint, jsonify, request
from datetime import datetime
from sqlalchemy import or_
from app.utils.auth import api_key_required
from app import db
from app.models import Client

# Initialize Blueprint for client-related routes
clients_bp = Blueprint('clients', __name__)

# Route for registering a new client
@clients_bp.route('/register', methods=['POST'])
@api_key_required
def register_client():
    """
    Registers a new client into the system. 
    This endpoint requires the user to be authenticated with an API key.
    """
    # Get the authenticated doctor's ID
    doctor = request.doctor
    doctor_id = doctor.id
    
    # Parse incoming JSON data
    data = request.get_json() or {}

    # Attempt to parse the client's date of birth (DOB)
    try:
        dob = datetime.strptime(data.get('date_of_birth'), '%Y-%m-%d').date() if data.get('date_of_birth') else None
    except ValueError:
        return jsonify({"msg": "Invalid date_of_birth format"}), 400

    # Create a new Client object with the provided data
    client = Client(
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        date_of_birth=dob,
        gender=data.get('gender'),
        contact_info=data.get('contact_info'),
        created_by_id=doctor_id  # Store the doctor's ID who created this client
    )

    # Validate required fields: first_name and last_name
    if not (client.first_name and client.last_name):
        return jsonify({"msg": "first_name and last_name required"}), 400

    # Save the new client to the database
    db.session.add(client)
    db.session.commit()

    # Return success message
    return jsonify({"message": "Client registered successfully"}), 200

# Route for listing all clients
@clients_bp.route('/', methods=['GET'])
@api_key_required
def list_clients():
    """
    Lists all registered clients in the system. 
    This endpoint requires the user to be authenticated with an API key.
    """
    # Query all clients from the database
    clients = Client.query.all()

    # Return a list of client IDs and names
    return jsonify([
        {"id": client.id, "first_name": client.first_name, "last_name": client.last_name}
        for client in clients
    ]), 200

# Route for searching clients by name
@clients_bp.route('/search', methods=['GET'])
@api_key_required
def search_clients():
    """
    Searches for clients based on a query string (first name or last name).
    This endpoint requires the user to be authenticated with an API key.
    """
    # Get the search query from request arguments
    q = request.args.get('q', '').strip()

    # Validate that a query string is provided
    if not q:
        return jsonify({"msg": "Query parameter 'q' is required"}), 400

    # Search for clients whose first or last name matches the query
    like = f"%{q}%"  # Using SQL 'LIKE' for partial matching
    matches = Client.query.filter(
        or_(Client.first_name.ilike(like), Client.last_name.ilike(like))
    ).all()

    # Return matched clients
    return jsonify([
        {"id": client.id, "first_name": client.first_name, "last_name": client.last_name}
        for client in matches
    ]), 200

# Route for fetching a client's full profile
@clients_bp.route('/<int:client_id>', methods=['GET'])
@api_key_required
def get_client_profile(client_id):
    """
    Retrieves a client's profile by ID, including the programs they are enrolled in.
    This endpoint requires the user to be authenticated with an API key.
    """
    # Fetch the client by ID or return 404 if not found
    client = Client.query.get_or_404(client_id)

    # Get the programs the client is enrolled in
    programs = [{
        "id": e.program.id,
        "name": e.program.name,
        "enrolled_at": e.enrolled_at.isoformat(),  # Date when the client enrolled
        "status": e.status  # Enrollment status
    } for e in client.enrollments]

    # Return the client's profile and their programs
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
        "programs": programs  # Include programs the client is enrolled in
    }), 200
