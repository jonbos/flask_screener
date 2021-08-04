"""
Blueprint for user functions and views
"""
from sqlite3 import IntegrityError

from flask import Blueprint, render_template, request, flash, redirect, url_for

from screener_app.auth import login_required
from screener_app.db import get_db

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/")
@login_required
def index():
    return render_template("user/index.html")


@bp.route("/add_favorite", methods=["POST"])
@login_required
def add_favorite():
    user_id = request.form.get('user_id')
    ticker = request.form.get("ticker")
    db = get_db()
    try:
        db.execute("INSERT INTO user_favorite (id_user, ticker) VALUES (?,?)",
                   (request.form.get('user_id'), request.form.get("ticker")))
        db.commit()
        flash(f"{ticker} added to your favorites!")
    except IntegrityError as e:
        flash(f"{ticker} is already in your favorites list!")
    return redirect(url_for('stocks.stock_api', ticker=ticker))
