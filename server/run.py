from app import create_app  # Import the app creation function from the app module

# Create an instance of the Flask app
app = create_app()

if __name__ == "__main__":
   
    # Set debug=True to enable debug mode
    app.run()
