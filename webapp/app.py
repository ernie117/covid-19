from pathlib import Path

import yaml
from flask import Flask, render_template, jsonify

from webapp.csv import etl_functions
from webapp.etl.dao import MongoDAO
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


@app.route("/json/<date>")
def json_for_date(date: str):
    result = MongoDAO("dates").get_one_document_by_date(date)
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
