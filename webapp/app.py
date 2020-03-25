from flask import Flask, render_template, jsonify

from webapp.data.extraction.countries_service import CountriesService
from webapp.data.transformation.covid_19_date_data import Covid19DateDataRTL
from webapp.data.transformation.document_to_dataframe import DocumentConverter
from webapp.services.dates_service import DatesService
from webapp.services.line_plotter import SeabornLinePlotter
from webapp.utils.utils import purge_images

DATES_SERVICE = DatesService()
COUNTRIES_SERVICE = CountriesService()

app = Flask(__name__)


@app.route("/<country>")
def home(country: str):
    purge_images()

    converter = DocumentConverter(DATES_SERVICE.get_dates_data(country))
    data = converter.convert_dates_to_dataframe()
    plotter = SeabornLinePlotter(data)
    plotter.set_seaborn_features()
    plotter.build_line_plot(country)

    return render_template("country.html",
                           country=country,
                           countries=get_countries())


@app.route("/function/update")
def update():
    return Covid19DateDataRTL().execute_rtl()


@app.route("/api/date/<date>")
def json_for_date(date: str):
    return jsonify(DATES_SERVICE.get_single_date(date))


@app.route("/api/country/<country>")
def json_for_country(country: str):
    return jsonify(DATES_SERVICE.get_dates_data(country))


@app.route("/countries")
def get_latest_countries():
    return jsonify(get_countries())


def get_countries():
    return COUNTRIES_SERVICE.get_latest_countries()


if __name__ == "__main__":
    app.run(debug=True)
