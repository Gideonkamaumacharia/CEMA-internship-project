"""
Initialize the Flask application and configure extensions.

This module sets up the Flask app instance, configures it based on the environment,
initializes database and migration tools, enables CORS, and registers all blueprints.

"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_cors import CORS
from .config import DevelopmentConfig, ProductionConfig, TestingConfig

# Initialize Flask extensions at the module level
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()


def create_app(config_class='app.config.Config'):
    """
    Create and configure the Flask application instance.

    Args:
        config_class (str): The configuration class to use. Default is the base Config.

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Determine environment and apply the corresponding configuration
    app_config = os.getenv('FLASK_ENV', 'development')  
    if app_config == 'production':
        app.config.from_object(ProductionConfig)
    elif app_config == 'testing':
        app.config.from_object(TestingConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # Initialize Flask extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CORS(app)  # Allow cross-origin requests for all API routes

    # Import and register blueprints
    from .routes import auth_bp, clients_bp, programs_bp, enroll_bp, admin_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(clients_bp, url_prefix='/api/clients')
    app.register_blueprint(programs_bp, url_prefix='/api/programs')
    app.register_blueprint(enroll_bp, url_prefix='/api/enrollments')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')

    return app
