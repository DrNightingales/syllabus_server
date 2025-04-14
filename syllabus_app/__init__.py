'''
Flask application factory
'''
from flask import Flask, current_app
from .models import init_db, init_app as init_db_app
from .routes import register_blueprints
from .config import Config
from .utils import render_markdown

def create_app() -> Flask:
    '''Creates and configures the Flask application instance.

    This factory function initializes the Flask app, configures it using the Config
    class, sets up the database, and registers the blueprints.

    Steps performed:
        1. Initialize Flask app with configuration from Config class
        2. Configure database using init_db and init_db_app
        3. Register blueprints via register_blueprints function

    Returns:
        Flask: The initialized Flask application instance
    '''

    app = Flask(__name__,
                template_folder=Config.TEMPLATE_FOLDER,
                static_folder=Config.STATIC_FOLDER
                )

    # Configure database path
    app.config.from_object(Config)
    app.add_template_filter(render_markdown, 'markdown')

    # Initialize database
    init_db(app)
    init_db_app(app)

    # Register blueprints
    register_blueprints(app)

    return app
