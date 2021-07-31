from flask import Blueprint, render_template

bp = Blueprint('stocks', __name__, url_prefix="/stocks")


@bp.route("", methods=("GET",))
def stock_index():
    return render_template("stocks/index.html")
