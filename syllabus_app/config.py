from pathlib import Path
import os


class Config:
    BASE_DIR = Path(os.path.abspath(os.path.dirname(__file__)))
    __current_file = Path(__file__)
    BASE_DIR = __current_file.parents[1]
    TEMPLATE_FOLDER = BASE_DIR / 'templates'
    STATIC_FOLDER = BASE_DIR / 'static'
    DATABASE = BASE_DIR / 'instance/syllabus.db'
    COURSES_DB_DIR = BASE_DIR / 'instance/courses'
    SECRET_KEY = 'secret'

    # General Flask settings
    DEBUG = True
    TESTING = False
