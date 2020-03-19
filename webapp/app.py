import os
from pathlib import Path

import yaml
from flask import Flask, render_template

from webapp.csv import etl_functions
from webapp.utils.utils import purge_images, check_for_existing_file, \
    get_countries

app = Flask(__name__)

with open(Path("config/config.yml"), "r") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)


@app.route("/<country>")
def home(country: str):
    purge_images()

    etl_functions.main(country.lower(),
                       Path("webapp/COVID-19-data"),
                       Path("webapp/static/images"))

    return render_template("index.html",
                           country=country,
                           countries=get_countries())


if __name__ == "__main__":
    app.run(debug=True)
