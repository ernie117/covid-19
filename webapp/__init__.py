from flask import Flask

from config.flask_config import DevConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig())

    with app.app_context():
        from webapp.views.dates import dates_blueprint

        app.register_blueprint(dates_blueprint)

    return app
