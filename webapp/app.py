from pathlib import Path

import yaml
from flask import Flask, render_template, jsonify

from webapp.csv import etl_functions
from webapp.etl.mongo_dao import MongoDAO
from webapp.services.dates_service import DatesService
from webapp.utils.utils import purge_images, get_countries

app = Flask(__name__)

with open(Path("config/config.yml"), "r") as f:
    app.config.update(
        yaml.load(f, Loader=yaml.FullLoader)
    )


@app.route("/<country>")
def home(country: str):
    purge_images()

    etl_functions.main(country.lower())

    return render_template("country.html",
                           country=country,
                           countries=get_countries())


@app.route("/api/date/<date>")
def json_for_date(date: str):
    return jsonify(DatesService().get_single_date(date))


@app.route("/api/country/<country>")
def json_for_country(country: str):
    return jsonify(DatesService().get_dates_data(country))


if __name__ == "__main__":
    app.run(debug=True)
