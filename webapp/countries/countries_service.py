"""
Holds the CountriesService class for dealing with the countries mongo
collection.
"""
from typing import List

from webapp.data.mongo.mongo_dao import MongoDAO
from webapp.utils.loggers import build_logger


class CountriesService:
    """
    Class that loads the most up-to-date countries from Mongo dates collection
    and persists to the Mongo countries collection.
    """

    def __init__(self):
        self.logger = build_logger("CountriesService")
        self.mongo_dates_dao = MongoDAO("dates")
        self.mongo_countries_dao = MongoDAO("countries")

    def get_latest_countries(self):
        """
        Loads the most up-to-date country list from the latest date document
        in the dates collection and persists it to the countries collection.
        Then returns that list of countries to serve as the menu in the flask
        app.
        """
        self._load_newest_countries()
        countries_document = self.mongo_countries_dao.get_all()
        countries_document = list(countries_document)

        return countries_document[0]["countries"]

    def _load_newest_countries(self):
        countries = self._get_most_up_to_date_countries()
        self._load_most_recent_countries(countries)

    def _get_most_up_to_date_countries(self) -> List:
        data_cursor = self.mongo_dates_dao.get_all()
        most_recent_entry = data_cursor.sort("date", -1).limit(1)

        countries = []
        for entry in list(most_recent_entry):
            country_array = entry["countries"]
            for obj in country_array:
                countries.append(obj["country/region"])

        return countries

    def _load_most_recent_countries(self, countries: List):
        self.mongo_countries_dao.collection.drop()

        document = {"countries": countries}
        result = self.mongo_countries_dao.insert_one_document(document)

        if result.acknowledged:
            self.logger.info(
                "Inserted list of %d countries to 'countries' collection",
                len(countries)
            )
        else:
            self.logger.warn("New countries not inserted!")
