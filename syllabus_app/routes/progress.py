from flask import Blueprint, render_template, request, redirect, url_for

bp = Blueprint(
    name="progress",
    import_name=__name__,
    url_prefix="/progress"
)


@bp.route('/')
def progress_hub() -> str:

    return render_template('progress.html')
