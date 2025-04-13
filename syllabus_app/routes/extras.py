'''
Extra materials routes
'''
from flask import Blueprint, render_template

bp = Blueprint('extras', __name__, url_prefix='/extras/<int:course_id>')


@bp.route('/new', methods=['GET', 'POST'])
def new_extra(course_id: int) -> str:
    # return render_template('extras/new_extra.html')
    return "Extra"


@bp.route('<int:extra_id>')
def extra_detail(course_id: int, extra_id: int) -> str:
    # return render_template('extras/extra_detail.html')
    return "Extra detail"
