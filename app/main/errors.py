from flask import render_template
from . import main


@main.app_errorhandler(404)
def page404(e):
    return render_template("errors/404.html"), 404

@main.app_errorhandler(403)
def page403(e):
    return render_template("errors/403.html"), 403

@main.app_errorhandler(500)
def page500(e):
    return render_template("errors/500.html"), 500
