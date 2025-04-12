"""
Extra materials routes
"""
from flask import Blueprint, render_template

bp = Blueprint('extras', __name__, url_prefix='/course/<int:course_id>')


@bp.route('/extra/new', methods=['GET', 'POST'])
def new_extra(course_id: int) -> str:
    return render_template('extras/new_extra.html')
