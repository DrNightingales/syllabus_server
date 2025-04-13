'''
Week-related routes
'''
from flask import Blueprint, render_template

bp = Blueprint('weeks', __name__, url_prefix='/weeks/<int:course_id>')


@bp.route('/new', methods=['GET', 'POST'])
def new_week(course_id: int) -> str:
    # return render_template('new_week.html', course_id=course_id)
    return "New week"


@bp.route('/<int:week_id>')
def week_detail(course_id: int, week_id: int) -> str:
    # return render_template('week_detail.html', course_id=course_id,
    # week_id=week_id)
    return "Week detail"
