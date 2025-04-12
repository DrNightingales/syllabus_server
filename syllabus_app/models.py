"""
Database models and initialization
"""
import sqlite3
from flask import g, current_app, Flask


def init_db(app: Flask) -> None:
    """Initialize database tables"""
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weeks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                week_number INTEGER,
                theory TEXT,
                problems TEXT,
                challenges TEXT,
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                title TEXT,
                content TEXT,
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                course_id INTEGER,
                week_number INTEGER,
                completed INTEGER DEFAULT 0,
                FOREIGN KEY(course_id) REFERENCES courses(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER,
                    start_week INTEGER,
                    end_week INTEGER,
                    completed INTEGER DEFAULT 0,
                    title TEXT,
                    content TEXT,
                    FOREIGN KEY(course_id) REFERENCES courses(id)

                )
        ''')

        db.commit()


def get_db() -> sqlite3.Connection:
    """Get database connection"""
    if 'db' not in g:
        g.db = sqlite3.connect(current_app.config['DATABASE'])
        print(type(g.db))
    return g.db


def close_db(e=None) -> None:
    """Close database connection"""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app: Flask) -> None:
    """Register database functions with app"""
    app.teardown_appcontext(close_db)
