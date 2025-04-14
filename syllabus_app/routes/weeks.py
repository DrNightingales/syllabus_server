'''
Week-related routes
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

bp = Blueprint('weeks', __name__, url_prefix='/weeks/<int:course_id>')


@bp.route('/new', methods=['GET', 'POST'])
def new_week(course_id: int) -> Response | str:
    '''Handle creation of new course week with optional problems/challenges.

    Raises:
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    '''    
    if request.method == 'POST':
        try:
            week_number = int(request.form.get('week_number', 0))
            theory_content = request.form.get('theory', '')
            
            # Get form data with empty list fallback
            problem_titles: list[str] = request.form.getlist('problems_titles[]')
            problem_contents: list[str] = request.form.getlist('problems_contents[]')
            challenge_titles: list[str] = request.form.getlist('challenges_titles[]')
            challenge_contents: list[str] = request.form.getlist('challenges_contents[]')

            # Validate input lengths
            if len(problem_titles) != len(problem_contents):
                raise ValueError("Problem titles and contents mismatch")
            if len(challenge_titles) != len(challenge_contents):
                raise ValueError("Challenge titles and contents mismatch")

            # Create dataclass instances
            week = Week(
                week_number=week_number,
                theory=theory_content,
                problems=[
                    Problem(title=t, content=c, solved=False)
                    for t, c in zip(problem_titles, problem_contents)
                ],
                challenges=[
                    Challenge(title=t, content=c, solved=False)
                    for t, c in zip(challenge_titles, challenge_contents)
                ]
            )

            # Database operations
            db_path = get_course_db_path(course_id)
            with sqlite3.connect(db_path) as conn:
                conn.execute('PRAGMA foreign_keys = ON')
                cursor = conn.cursor()

                # Insert week
                cursor.execute('''
                    INSERT INTO weeks (week_number, theory)
                    VALUES (?, ?)
                    ON CONFLICT(week_number) DO UPDATE SET
                        theory = excluded.theory
                ''', (week.week_number, week.theory))

                # Clear existing problems/challenges for update case
                cursor.execute('DELETE FROM problems WHERE week_number = ?', (week.week_number,))
                cursor.execute('DELETE FROM challenges WHERE week_number = ?', (week.week_number,))

                # Insert problems
                for problem in week.problems:
                    cursor.execute('''
                        INSERT INTO problems 
                        (week_number, title, content, solved)
                        VALUES (?, ?, ?, ?)
                    ''', (week.week_number, problem.title, problem.content, 0))

                # Insert challenges
                for challenge in week.challenges:
                    cursor.execute('''
                        INSERT INTO challenges 
                        (week_number, title, content, solved)
                        VALUES (?, ?, ?, ?)
                    ''', (week.week_number, challenge.title, challenge.content, 0))


            flash('Week created/updated successfully', 'success')
            return redirect(url_for('courses.course_detail', course_id=course_id))

        except (ValueError, sqlite3.Error) as e:
            current_app.logger.error(f"Week creation failed: {str(e)}")
            flash(f'Error creating week: {str(e)}', 'error')
            return redirect(request.referrer or 
                        url_for('weeks.new_week', course_id=course_id))
    return render_template('weeks/new_week.html', course_id=course_id)

@bp.route('/<int:week_number>')
def week_detail(course_id: int, week_number: int) -> str:
    # return render_template('week_detail.html', course_id=course_id,
    # week_id=week_id)
    return "Week detail"
