"""
Contains the class acting as intermediary between the Mongo dates collection and
calling code.
"""
import datetime
from typing import Dict, List

from webapp.data.loading.mongo_dao import MongoDAO
from webapp.loggers.loggers import build_logger

LOGGER = build_logger("DatesService")


class DatesService:
    """
    todo
    """

    def __init__(self):
        self.mongo_dao = MongoDAO("dates")

    def get_dates_data(self, country: str) -> List[Dict]:
        """
        todo
        :param country:
        :return:
        """
        data = list(self.mongo_dao.get_all_dates_by_country(country))
        LOGGER.info("Retrieved %d date documents.", len(data))

        return list(filter(lambda d: d["cases"], data))

    def get_single_date(self, date: str):
        """
        todo
        :param date:
        :return:
        """
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        data = self.mongo_dao.get_one_document_by_date(date_obj)

        return data if data else {"not found": "no data for that date"}

    def insert_multiple_dates(self, dates: list):
        """
        todo
        :param dates:
        :return:
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

    def _convert_dates_data(self):
        """
        todo
        :return:
        """
        pass
