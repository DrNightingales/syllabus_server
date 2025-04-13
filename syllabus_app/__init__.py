'''
Flask application factory
'''
from flask import Flask, current_app
from .models import init_db, init_app as init_db_app
from .routes import register_blueprints
from .config import Config


def create_app() -> Flask:
    '''Application factory function'''

    app = Flask(__name__,
                template_folder=Config.TEMPLATE_FOLDER,
                static_folder=Config.STATIC_FOLDER
                )

    # Configure database path
    app.config.from_object(Config)

    # Initialize database
    init_db(app)
    init_db_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
