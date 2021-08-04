"""
App factory
"""

import os

from flask import Flask

from screener_app import stock, user
from screener_app.stock import stock_info


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, "blog.sqlite")
    )

    @app.route('/')
    def index():
        return stock_info()

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    # IoC
    db.init_app(app)

    # register blueprints
    from screener_app import stock, auth

    app.register_blueprint(stock.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    return app
