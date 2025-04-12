"""
Route blueprint registration
"""
from flask import Blueprint, Flask


def register_blueprints(app: Flask):
    """Register all blueprints with the app"""
    from . import courses, weeks, extras, progress
    app.register_blueprint(courses.bp)
    app.register_blueprint(weeks.bp)
    app.register_blueprint(extras.bp)
    app.register_blueprint(progress.bp)
