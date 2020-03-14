import os

import yaml
from flask import Flask, render_template

from webapp.functions import etl_functions

app = Flask(__name__)

with open("config\\config.yml", "r") as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)


@app.route("/<country>")
def home(country: str):
    country = country.lower()

    if not check_for_existing_file(country):
        etl_functions.main(country,
                           CONFIG["directories"]["covid19Directory"],
                           CONFIG["directories"]["plotImgDirectory"])

    return render_template("index.html", country=country)


def check_for_existing_file(country: str):
    with os.scandir("static\\images") as iterator:
        for filename in iterator:
            if filename.name.split(".")[0] == country:
                return filename.name

    return None


if __name__ == "__main__":
    app.run(debug=True)
