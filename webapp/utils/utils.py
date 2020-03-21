import csv
import os
from pathlib import Path

from webapp.etl.country_transformer import CountryTransformer


def check_for_existing_file(country: str):
    with os.scandir(Path("webapp/static/images")) as iterator:
        for filename in iterator:
            if filename.name.split(".")[0] == country:
                return filename.name

    return None


def get_countries():
    countries = []
    filter_countries = [
        "Gibraltar", "Channel Islands", "Occupied Palestinian Territory"
    ]
    with os.scandir(Path("webapp/COVID-19-data")) as iterator:
        for filename in iterator:
            if filename.name.endswith("csv"):
                with open(Path("webapp/COVID-19-data/" + filename.name),
                          "r") as f:
                    data = csv.DictReader(f)
                    for thing in data:
                        if thing["Country/Region"] in filter_countries:
                            continue
                        countries.append(thing["Country/Region"])

    return sorted({CountryTransformer(country).transform()
                   for country in countries})


def purge_images():
    with os.scandir(Path("webapp/static/images")) as iterator:
        for filename in iterator:
            if filename.name.endswith("png"):
                os.remove(filename)
