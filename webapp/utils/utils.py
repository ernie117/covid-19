import csv
import os


def check_for_existing_file(country: str):
    with os.scandir("webapp/static/images") as iterator:
        for filename in iterator:
            if filename.name.split(".")[0] == country:
                return filename.name

    return None


def get_countries():
    countries = []
    filter_countries = ("Gibraltar", "Channel Islands")
    with os.scandir("webapp/COVID-19-data") as iterator:
        for filename in iterator:
            if filename.name.endswith("csv"):
                with open("webapp/COVID-19-data/" + filename.name, "r") as f:
                    data = csv.DictReader(f)
                    for thing in data:
                        countries.append(thing["Country/Region"])

    return sorted([country for country in set(countries)
                   if country not in filter_countries])


def purge_images():
    with os.scandir("webapp/static/images") as iterator:
        for filename in iterator:
            if filename.name.endswith("png"):
                os.remove(filename)
