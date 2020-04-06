"""
Routes for the RESTful API endpoints of the application.
"""
from flask import Blueprint, jsonify

from webapp.countries.countries_service import CountriesService
from webapp.dates.dates_service import DatesService

DATES_SERVICE = DatesService()
COUNTRIES_SERVICE = CountriesService()

restful = Blueprint("restful", __name__)


@restful.route("/api/date/<date>")
def json_for_date(date: str):
    return jsonify(DATES_SERVICE.get_single_date(date))


@restful.route("/api/country/<country>")
def json_for_country(country: str):
    return jsonify(DATES_SERVICE.get_dates_data(country))


@restful.route("/api/countries")
def get_latest_countries():
    return jsonify(COUNTRIES_SERVICE.get_latest_countries())
