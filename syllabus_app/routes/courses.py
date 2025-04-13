'''
Course management routes including import/export functionality
'''
from flask import Blueprint, \
    render_template, \
    request, \
    redirect, \
    url_for, \
    send_file, \
    current_app, \
    flash
from werkzeug.wrappers.response import Response
from pathlib import Path
import sqlite3
from ..datatypes import *
from ..models import get_db
from ..utils import get_course_progress
from ..course_operations import export_course_data, \
    get_course_db_path, \
    get_the_last_course_id, \
    create_course_in_main_db, \
    create_course_db

bp = Blueprint('courses', __name__, url_prefix='/courses')


@bp.route('/')
def index() -> str:
    db = get_db()
    courses = db.execute(
        "SELECT id, title, progress FROM courses ORDER BY id").fetchall()

    course_list = []
    for course in courses:
        course_list.append(CoursePreview(**course))
    return render_template('courses/index.html', courses=course_list)


@bp.route('/<int:course_id>')
def course_detail(course_id: int) -> Response | str:

    # Check if the course with the given id is in the main database
    db = get_db()
    course = db.execute(
        'SELECT id, title FROM courses WHERE id = ?',
        (course_id,)
    ).fetchone()[0]
    if not course:
        return redirect(url_for('courses.index'))

    try:
        course = export_course_data(course_id)
    except FileNotFoundError:
        course = Course
    return render_template('courses/detail.html', course=course, course_id=course_id)


@bp.route('/new', methods=['GET', 'POST'])
def new_course():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            return render_template(
                'courses/new.html',
                error="Title is required")
        try:
            course_id = create_course_in_main_db(title)
            create_course_db(course_id, title, description)
            return redirect(url_for('courses.index'))
        except sqlite3.Error as e:
            flash(f"Error creating course: {str(e.args)}\n{type(e)}", 'error')
            return render_template('courses/new_course.html')

    return render_template('courses/new_course.html')


@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    db = get_db()
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()

        if not title:
            course = db.execute(
                'SELECT * FROM courses WHERE id = ?', (course_id,)).fetchone()
            return render_template(
                'courses/edit.html',
                course=course,
                error="Title is required")

        db.execute(
            'UPDATE courses SET title = ?, description = ? WHERE id = ?',
            (title, description, course_id)
        )
        db.commit()
        return redirect(url_for('courses.course_detail', course_id=course_id))

    course = db.execute('SELECT * FROM courses WHERE id = ?',
                        (course_id,)).fetchone()
    return render_template('courses/edit.html', course=course)


@bp.route('/<int:course_id>/delete')
def delete_course(course_id: int) -> str:
    return render_template('courses/delete.html')


@bp.route('/<int:course_id>/export', methods=['GET'])
def export_course(course_id: int) -> Response:
    return send_file(
        path_or_file=get_course_db_path(course_id),
        mimetype="application/octet-stream",
        as_attachment=True,
        download_name=f"course_{course_id}.db"
    )


@bp.route('/import', methods=['POST'])
def import_course() -> Response | tuple[str, int]:
    if 'file' not in request.files:
        return "No file part in the request", 400

    file = request.files['file']

    if file.filename == '':
        return "No file selected", 400

    filepath = Path(current_app.config['COURSES_DB_DIR']
                    ) / f"course_{get_the_last_course_id() + 1}.db"
    file.save(filepath)
    return redirect(url_for('courses.index'))
