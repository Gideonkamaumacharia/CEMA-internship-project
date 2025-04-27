from app import create_app  # Import the app creation function from the app module

# Create an instance of the Flask app
app = create_app()

if __name__ == "__main__":
    # Run the app in debug mode (for development)
    app.run(debug=True)
