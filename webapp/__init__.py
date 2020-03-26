from flask import Flask

from config.flask_config import DevConfig
from . import routes


def create_app():
    app = Flask(__name__)

    with app.app_context():
        app.config.from_object(DevConfig())
        from . import routes

        app.register_blueprint(routes.data_page)

        return app
