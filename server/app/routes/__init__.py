"""
Initialize and expose all route blueprints.

This file imports the individual blueprints from the route modules
(clients, programs, enrollments, authentication, and admin) and makes them available
for registration in the application factory.
"""

from .clients import clients_bp
from .programs import programs_bp
from .enrollments import enroll_bp
from .auth import auth_bp
from .admin import admin_bp
