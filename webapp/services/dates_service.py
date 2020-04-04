"""
Contains the class acting as intermediary between the Mongo dates collection and
calling code.
"""
import datetime
from typing import Dict, List, Optional

from pymongo.results import InsertManyResult

from webapp.data.loading.mongo_dao import MongoDAO
from webapp.loggers.loggers import build_logger

LOGGER = build_logger("DatesService")


class DatesService:
    """
    Acts as intermediary service layer between a MongoDAO and calling code at
    the view layer.
    """

    def __init__(self):
        self.mongo_dao = MongoDAO("dates")

    def get_dates_data(self, country: str) -> List[Dict]:
        """
        Uses MongoDAO to retrieve date data for a specified country and pass to
        the list constructor. Also filters out dates with no cases.

        :param country: String representing country.
        :return: A list of date documents
        """
        data = list(self.mongo_dao.get_all_dates_by_country(country))
        LOGGER.info("Retrieved %d date documents.", len(data))

        return list(filter(lambda d: d["cases"], data))

    def get_single_date(self, date: str) -> Dict:
        """
        Uses MongoDAO to retrieve data for a single specified date, or custom
        object if not found.

        :param date: String representing date to search.
        :return: Date document if found.
        """
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        data = self.mongo_dao.get_one_document_by_date(date_obj)

        return data if data else {"not found": "no data for that date"}

    def insert_multiple_dates(self, dates: list) -> Optional[InsertManyResult]:
        """
        Uses MongoDAO to insert 1 to n new documents of transformed data
        requested from covid-19 data repo.

        :param dates: A list of documents to insert.
        :return: InsertManyResult object describing our insert success.
        """
        if not dates:
            LOGGER.info("No Documents to insert!")
            return

        result = self.mongo_dao.insert_many_documents(dates)
        if result.acknowledged:
            LOGGER.info("Documents inserted successfully!")
        else:
            LOGGER.info("Documents not inserted!")

        return result if result else None

