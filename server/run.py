from app import create_app
import logging
#from app.models import Doctor, Client, HealthProgram, Enrollment
from flask import request,Blueprint

# Create an app instance and run it
app = create_app()
#main_bp = Blueprint('main',__name__)

##app = create_app(config_class='app.config.DevelopmentConfig')

#logging.basicConfig(level=logging.DEBUG)  
#app.logger.setLevel(logging.DEBUG)

##@main_bp.before_request
#def log_request():
    #app.logger.info(f"Incoming request: {request.method} {request.url} - {request.get_json()}")


if __name__ == "__main__":
    app.run(debug=True)
