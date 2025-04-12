"""
Application entry point
"""
from syllabus_app import create_app
from flask import redirect, url_for, current_app
app = create_app()


@app.route('/')
def index():
    # Redirect to the courses blueprint's root route
    return redirect(url_for('courses.index'))


if __name__ == '__main__':
    app.run(debug=True)
