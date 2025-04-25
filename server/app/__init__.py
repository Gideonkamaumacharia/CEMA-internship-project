from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
import os
from flask_cors import CORS
from .config import DevelopmentConfig, ProductionConfig, TestingConfig  

# Module-level instances let the entire codebase refer to db, bcrypt, jwt, and migrate without yet assigning them to the app
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()
migrate = Migrate()


def create_app(config_class='app.config.Config'):
    app = Flask(__name__)

    # Determine the environment and set the configuration
    app_config = os.getenv('FLASK_ENV', 'development')  # Default to 'development' if not set
    if app_config == 'production':
        app.config.from_object(ProductionConfig)
    elif app_config == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)
    
    # init_app calls bind the instances to the app, wiring them up with configuration, blueprints, and the application context.
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
  
    CORS(app)


    # Register the routes with the SQLAlchemy instance
    # Register blueprints from the /routes package
    from .routes import auth_bp, clients_bp, programs_bp, enroll_bp
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(programs_bp, url_prefix='/api/programs')
    app.register_blueprint(enroll_bp, url_prefix='/api/enrollments')

    #print(app.url_map)

    return app
