from flask import Flask

from config.flask_config import DevConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevConfig())

    with app.app_context():
        from webapp.dates.routes import dates
        # from webapp.countries.routes import countries
        from webapp.rest.routes import restful

        app.register_blueprint(dates)
        # app.register_blueprint(countries)
        app.register_blueprint(restful)

    return app
