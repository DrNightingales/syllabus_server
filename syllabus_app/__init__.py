"""
Flask application factory
"""
from flask import Flask, current_app
import os
from .models import init_db, init_app as init_db_app
from .routes import register_blueprints
from pathlib import Path


def create_app() -> Flask:
    """Application factory function"""
    current_file = Path(__file__)
    home_dir = current_file.parents[1]
    template_dir = home_dir.joinpath('templates')
    static_dir = home_dir.joinpath('static')
    database_path = home_dir.joinpath('syllabus.db')

    app = Flask(
        __name__,
        template_folder=template_dir,  # Explicit templates path
        static_folder=static_dir  # Static folder
    )

    # Configure database path
    app.config['DATABASE'] = database_path

    # Initialize database
    init_db(app)
    init_db_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
