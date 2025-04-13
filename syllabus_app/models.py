'''
Database models and initialization for main application and course-specific databases
'''
from flask import current_app, g
from pathlib import Path
import sqlite3
from flask import Flask


# --- Main Application Database Models ---
def init_db(app: Flask) -> None:
    '''Initialize the main application database tables'''
    with app.app_context():
        db = get_db()
        with db:
            db.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    progress REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')


def get_db() -> sqlite3.Connection:
    '''Get the main application database connection'''
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None) -> None:
    '''Close the main database connection'''
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app: Flask) -> None:
    '''Register database functions with the Flask application'''
    app.teardown_appcontext(close_db)
