import sys
import os
from app import create_app

# Check the current working directory and sys.path for debugging purposes
print("sys.path:", sys.path)
print("Current working directory:", os.getcwd())

# Set the Flask environment to production or development
env = os.getenv("FLASK_ENV", "production")  # Default to 'production' if not set
print("Running in:", env)

# Create the app instance
app = create_app()

if __name__ == "__main__":
    # Run the app with debug mode based on the environment variable
    app.run(debug=(env == "development"))
