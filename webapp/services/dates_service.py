"""
Contains the class acting as intermediary between Mongo dates collection and
calling code.
"""
import datetime

from webapp.etl.mongo_dao import MongoDAO
from webapp.loggers.loggers import build_logger


class DatesService:
    """
    todo
    """

    def __init__(self):
        self.mongo_dao = MongoDAO("dates")
        self.logger = build_logger("DatesService")

    def get_dates_data(self, country: str):
        """
        todo
        :param country:
        :return:
        """
        data = self.mongo_dao.get_all_dates_by_country(country)
        self.logger.info("Retrieved %d date documents.", len(data))

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
            self.logger.info("No Documents to insert!")
            return

        result = self.mongo_dao.insert_many_documents(dates)
        if result.acknowledged:
            self.logger.info("Documents inserted successfully!")
        else:
            self.logger.info("Documents not inserted!")

        return result if result else None

    def _convert_dates_data(self):
        """
        todo
        :return:
        """
        pass
