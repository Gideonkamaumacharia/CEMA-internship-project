"""
Configuration module for the Flask application.

This file sets up the configuration classes for different environments: 
Development, Production, and Testing.
"""

import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Define the base directory of the application
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class with default settings.
    Other configurations will inherit from this class.
    """
    SECRET_KEY = os.urandom(24)  # Secret key for securely signing the session cookie
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal tracking for performance
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Default database URI

    # Email settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_USERNAME')


class DevelopmentConfig(Config):
    """
    Configuration for development environment.
    """
    DEBUG = True
    ENV = 'development'
    # Optional: Override database URI for development
    # SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'postgresql://graduate_db_user:simplepassword123@localhost/graduate_db')


class ProductionConfig(Config):
    """
    Configuration for production environment.
    """
    DEBUG = False
    ENV = 'production'
    # Optional: Production-specific database URI can be set here
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class TestingConfig(Config):
    """
    Configuration for testing environment.
    """
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'  # Use lightweight SQLite database for tests
