'''
Utility functions
'''
from .models import get_db
from datetime import datetime

def get_course_progress(course_id) -> float:
    '''Calculate course completion percentage

    Returns:
        float: completion percentage
    '''    
    db = get_db()
    total_weeks = db.execute(
        'SELECT COUNT(*) FROM weeks WHERE course_id = ?',
        (course_id,
         )).fetchone()[0]
    completed_weeks = db.execute('''
        SELECT COUNT(*) FROM progress
        WHERE course_id = ? AND completed = 1
    ''', (course_id,)).fetchone()[0]
    return completed_weeks / total_weeks if total_weeks > 0 else 0.0

def convert_timestamp(value: bytes) -> datetime:
    '''Converts sqlite TIMESTAMP to datetime

    Args:
        value (bytes): TIMESTAMP

    Returns:
        datetime
    '''    
    return datetime.strptime(value.decode('utf-8'), '%Y-%m-%d %H:%M:%S')

