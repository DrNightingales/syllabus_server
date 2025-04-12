"""
Week-related routes
"""
from flask import Blueprint, render_template

bp = Blueprint('weeks', __name__, url_prefix='/course/<int:course_id>')


@bp.route('/week/new', methods=['GET', 'POST'])
def new_week(course_id: int) -> str:
    return render_template('new_week.html', course_id=course_id)
