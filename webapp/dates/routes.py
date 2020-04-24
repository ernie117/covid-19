from flask import render_template, Blueprint

from webapp.countries.countries_service import CountriesService
from webapp.data.transformation.covid_19_date_data import Covid19DateDataRTL
from webapp.data.transformation.document_to_dataframe import DocumentConverter
from webapp.dates.dates_service import DatesService
from webapp.plotting.line_plotter import SeabornLinePlotter
from webapp.utils.utils import purge_images

DATES_SERVICE = DatesService()
COUNTRIES_SERVICE = CountriesService()

dates = Blueprint("dates", __name__)


@dates.route("/dates/<country>")
def home(country: str):
    purge_images()

    converter = DocumentConverter(DATES_SERVICE.get_dates_data(country))
    data = converter.convert_dates_to_dataframe()
    plotter = SeabornLinePlotter(data)
    plotter.set_seaborn_features()
    plotter.build_line_plot(country)

    return render_template(
        "country.html",
        country=country,
        countries=COUNTRIES_SERVICE.get_latest_countries(),
    )


# This option will be on the home page eventually
@dates.route("/function/update")
def update():
    return Covid19DateDataRTL().execute_rtl()
