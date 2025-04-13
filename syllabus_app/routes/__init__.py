'''
Route blueprint registration
'''
from flask import Flask, redirect, url_for


def register_blueprints(app: Flask) -> None:
    '''Register all blueprints with the app'''
    from . import courses, weeks, extras, progress, projects
    app.register_blueprint(courses.bp)
    app.register_blueprint(weeks.bp)
    app.register_blueprint(extras.bp)
    app.register_blueprint(progress.bp)
    app.register_blueprint(projects.bp)

    @app.route('/')
    def index():
        # Redirect to the courses blueprint's root route
        return redirect(url_for('courses.index'))
