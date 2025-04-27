from app import create_app, db
from app.models import Doctor, APIKey
import secrets

def seed_superadmin():
    """
    This script is designed to seed the database with a super admin user and generate their API key.
    It allows for the seeding of a super admin (doctor) with a unique API key, which is required for accessing protected routes in the app.

    It also prompts the user for the super admin’s name and email and then seeds the database if the super admin doesn't already exist.

    The script also generates an API key for the super admin and prints it to the console. This API key will be required when making API requests for creating other doctors or doing other administartive roles like creating programs.

    
    This is a one-time setup process.
    """
    # Initialize the Flask application and create the app context
    app = create_app()

    # Use the app context to access the database
    with app.app_context():
        """" 
        The script uses input() to collect the super admin’s name and email from the user.
        """

        # Prompt for the super admin's name and email
        superadmin_name = input("Enter the super admin's name: ").strip()
        superadmin_email = input("Enter the super admin's email: ").strip()

        """     
        If a doctor with the provided email already exists, their API key is displayed.

    """
        # Check if a doctor with this email already exists
        doctor = Doctor.query.filter_by(email=superadmin_email).first()

        """If the super admin does not exist, a new doctor is created with the provided details and marked as an admin (is_admin=True). """

        # If no doctor exists, create a new one as the super admin
        if not doctor:
            doctor = Doctor(name=superadmin_name, email=superadmin_email, is_admin=True)
            db.session.add(doctor)
            db.session.commit()
            print(f"Super admin '{superadmin_name}' seeded successfully.")

        # Check if the doctor already has an associated API key
        if not doctor.api_keys:
            "" " The API key is generated using Python's secrets.token_hex(32), which ensures that the key is randomly generated and secure."""
            # Generate a new API key for the super admin
            key = secrets.token_hex(32)  # Securely generate a random API key
            api_key = APIKey(key=key, doctor=doctor)
            db.session.add(api_key)
            db.session.commit()
            print(f"API Key for '{superadmin_name}': {key}")
        else:
            # If an API key already exists, print it
            print(f"Existing API Key for '{superadmin_name}': {doctor.api_keys[0].key}")

if __name__ == "__main__":
    seed_superadmin()
