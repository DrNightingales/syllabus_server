'''
Core operations for course import/export and management
'''
import sqlite3
from pathlib import Path
from typing import Any
from flask import current_app
from .datatypes import Problem, \
    Project, \
    Challenge, \
    Week, \
    Extra, \
    Meta, \
    Course


def create_course_in_main_db(title: str) -> int:
    '''
    Create a course entry in the main application database and return the new course ID.

    Args:
        title: The title of the course
        description: Optional description of the course

    Returns:
        The newly created course ID
    '''
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO courses (title) VALUES (?)",
            (title,)
        )
        course_id = cursor.lastrowid if cursor.lastrowid else 0

        conn.commit()

    return course_id


def get_the_last_course_id() -> int:
    '''
    Get the ID of the most recently created course from the main database.

    This function connects to the main application database and retrieves
    the row ID of the last inserted course record. This is typically used
    to get the ID of a newly created course.

    Returns:
        int: The ID of the last inserted course, or None if no courses exist.

    Raises:
        sqlite3.Error: If there is any database error during the operation.
    '''
    with sqlite3.connect(current_app.config['DATABASE']) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM courses")
        latest_id = cursor.fetchone()[0]

    return latest_id


def create_course_db(course_id: int, title: str, description: str) -> Path:
    '''Creates a database for a new course

    Args:
        course_id (int): id of the course in the main database
        title (str): course title
        description (str): course description

    Returns:
        Path: Path for the location of the newly created database
    '''    
    db_path = get_course_db_path(course_id)

    with sqlite3.connect(db_path) as conn:
        conn.execute('PRAGMA foreign_keys = ON')

        # Meta information about the course
        conn.execute('''
            CREATE TABLE meta (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Fill in the  meta info for the course
        conn.execute('INSERT INTO meta (title, description) VALUES (?, ?)',
                     (title, description))

        # Weekly content structure
        conn.execute('''
            CREATE TABLE weeks (
                week_number INTEGER PRIMARY KEY,
                completed INTEGER DEFAULT 0,
                theory TEXT
            )
        ''')

        # Problems and challenges for each week
        conn.execute('''
            CREATE TABLE problems (
                id INTEGER PRIMARY KEY,
                week_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                solved INTEGER DEFAULT 0,
                FOREIGN KEY(week_number) REFERENCES weeks(week_number)
            )
        ''')

        conn.execute('''
            CREATE TABLE challenges (
                id INTEGER PRIMARY KEY,
                week_number INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                solved INTEGER DEFAULT 0,
                FOREIGN KEY(week_number) REFERENCES weeks(week_number)
            )
        ''')

        # Course projects spanning multiple weeks
        conn.execute('''
            CREATE TABLE projects (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                start_week INTEGER NOT NULL,
                end_week INTEGER NOT NULL,
                finished INTEGER DEFAULT 0,
                FOREIGN KEY(start_week) REFERENCES weeks(week_number),
                FOREIGN KEY(end_week) REFERENCES weeks(week_number)
            )
        ''')

        # Additional course materials
        conn.execute('''
            CREATE TABLE extras (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        ''')

    return db_path


def export_course_data(course_id: int) -> Course:
    '''Export course data to a structured dictionary'''
    db_path = get_course_db_path(course_id)
    if not db_path.exists():
        raise FileNotFoundError(f"Course database {db_path} not found")

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Get course metadata
        meta_row = cursor.execute(
            "SELECT title, description, created_at FROM meta").fetchone()
        print(meta_row)
        meta = Meta(**meta_row)

        # Get weeks data
        cursor.execute(
            "SELECT theory, completed, week_number FROM weeks ORDER BY week_number")
        weeks = []
        for week in cursor.fetchall():
            weeks.append(Week(**week))

            # Get problems for this week
            cursor.execute(
                "SELECT title, content, solved FROM problems WHERE week_number = ?",
                (week['week_number']))
            weeks[-1].problems = [Problem(**p) for p in cursor.fetchall()]

            # Get challenges for this week
            cursor.execute(
                "SELECT title, content, solved FROM challenges WHERE week_number = ?",
                (week['week_number'],))
            weeks[-1].challenges = [Challenge(**c) for c in cursor.fetchall()]

        # Get projects
        cursor.execute(
            "SELECT title, content, start_week, end_week, finished FROM projects")
        projects = [Project(**p) for p in cursor.fetchall()]

        # Get extra materials
        cursor.execute("SELECT title, content FROM extras")
        extras = [Extra(**e) for e in cursor.fetchall()]

        course = Course(meta, weeks, projects, extras)

    return course


def import_course_data(course: Course) -> int:
    '''Import course data and return new course ID

    Returns:
        course_id(int): Imported course id in the main database
    '''    
    # First create the course in main database to get ID
    course_id = create_course_in_main_db(course.title)

    # Create course-specific database
    db_path = create_course_db(course_id, 
                               course.title, 
                               course.description)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Insert weeks data
        for week in course.weeks:
            cursor.execute(
                "INSERT INTO weeks (week_number, theory, completed) VALUES (?, ?, ?)",
                (week.number, week.theory, int(week.completed)))

            # Insert problems
            for problem in week.problems:
                cursor.execute(
                    "INSERT INTO problems (week_number, title, content, solved) VALUES (?, ?, ?, ?)",
                    (week.number,
                     problem.title,
                     problem.content,
                     int(problem.solved))
                )

            # Insert challenges
            for challenge in week.challenges:
                cursor.execute(
                    "INSERT INTO challenges (week_number, title, content, solved) VALUES (?, ?, ?, ?)",
                    (week.number,
                    challenge.title,
                    challenge.content,
                    int(challenge.solved)))

        # Insert projects
        for project in course.projects:
            cursor.execute(
                "INSERT INTO projects (title, content, start_week, end_week, finished) VALUES (?, ?, ?, ?, ?)",
                (project.title,
                project.content,
                project.start_week,
                project.end_week,
                project.finished))

        # Insert extras
        for extra in course.extras:
            cursor.execute(
                "INSERT INTO extras (title, content) VALUES (?, ?)",
                (extra.title, extra.content)
            )

        conn.commit()
        return course_id


def get_course_db_path(course_id: int) -> Path:
    '''Get path to course-specific database'''
    return Path(current_app.config['COURSES_DB_DIR']
                ) / f"course_{course_id}.db"
