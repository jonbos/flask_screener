from flask import Blueprint, render_template

from screener_app.auth import login_required

bp = Blueprint("user", __name__, url_prefix="/user")

@bp.route("/")
@login_required
def index():
    return render_template("user/index.html")
