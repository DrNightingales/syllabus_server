'''
Projects management routres
'''
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, send_file, Response, current_app
from pathlib import Path
import sqlite3
from ..models import get_db
from ..utils import get_course_progress
from ..course_operations import export_course_data, import_course_data, get_course_db_path, get_the_last_course_id

bp = Blueprint('projects', __name__, url_prefix='/projects/<int:course_id>')


@bp.route("/<int:project_id>")
def project_detail(course_id: int, project_id: int) -> str:
    db_path = get_course_db_path(course_id)
    with sqlite3.connect(db_path) as conn:
        project = dict(conn.execute(
            "SELECT * FROM projects WHERE id = ?", (project_id,)).fetchone())
        return str(project)


@bp.route("/new")
def new_project(course_id: int) -> str:
    db_path = get_course_db_path(course_id)
    with sqlite3.connect(db_path) as conn:
        res = conn.cursor().execute(
            '''SELECT MAX(id) FROM projects''').fetchone()[0]
        return f"New project id is {int(res) + 1}"
