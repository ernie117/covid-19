from flask import Flask

from config.flask_config import DevConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig())

    with app.app_context():
        from .routes import data_page

        app.register_blueprint(data_page)

    return app
