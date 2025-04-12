from flask import Blueprint, render_template, request, redirect, url_for, current_app
import os
from ..models import get_db
from ..utils import get_course_progress
import sqlite3

bp = Blueprint('courses', __name__, url_prefix='/courses')


def create_course_db(course_id: int) -> None:
    """
    Create a separate SQLite database file for the course,
    and initialize it with required tables.
    """
    # Construct the path to the new course database file.
    # Here, we store it in the app's instance folder.
    db_filename = f"course_{course_id}.db"
    db_path = os.path.join(current_app.instance_path, db_filename)

    # Ensure the instance folder exists.
    os.makedirs(current_app.instance_path, exist_ok=True)

    # Connect to the new database.
    conn = sqlite3.connect(db_path)
    with conn:
        cur = conn.cursor()
        # Create tables for problems, extras, and progress.
        cur.exeute('''
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT
                -- Add more columns as needed.
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS extras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                content TEXT
                -- Add more columns as needed.
            )
        ''')
        cur.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_number INTEGER,
                completed INTEGER DEFAULT 0
                -- Add more columns as needed.
            )
        ''')
        # Optionally, you can also create a table for projects:
        cur.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                start_week INTEGER,
                end_week INTEGER,
                completed INTEGER DEFAULT 0,
                title TEXT,
                content TEXT
            )
        ''')
    conn.close()


@bp.route('/')
def index() -> str:
    db = get_db()
    courses = db.execute("SELECT * FROM courses").fetchall()
    course_progress = {course[0]: get_course_progress(
        course[0]) for course in courses}
    return render_template('index.html', courses=courses, course_progress=course_progress)


@bp.route('/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'INSERT INTO courses (title, description) VALUES (?, ?)',
            (request.form['title'], request.form['description'])
        )
        db.commit()
        return redirect(url_for('courses.index'))
    return render_template('new_course.html')


@bp.route('/<int:course_id>')
def course_detail(course_id: int) -> str:
    db = get_db()
    course = db.execute('SELECT * FROM courses WHERE id = ?',
                        (course_id,)).fetchone()
    if not course:
        return redirect(url_for('courses.index'))
    return render_template('course_detail.html', course=course)


@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    db = get_db()
    if request.method == 'POST':
        db.execute(
            'UPDATE courses SET title = ?, description = ? WHERE id = ?',
            (request.form['title'], request.form['description'], course_id)
        )
        db.commit()
        return redirect(url_for('courses.course_detail', course_id=course_id))

    course = db.execute('SELECT * FROM courses WHERE id = ?',
                        (course_id,)).fetchone()
    return render_template('edit_course.html', course=course)


@bp.route('/<int:course_id>/delete')
def delete_course(course_id: int) -> str:
    return render_template('delete_course.html')
