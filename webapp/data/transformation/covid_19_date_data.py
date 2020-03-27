"""
Contains a class that acts as an abstraction layer in front of all the extract,
transform and load logic. CSV data is requested from github, transformed into
objects organised by date and loaded into mongoDB.
"""
from typing import Dict

from pymongo.results import InsertManyResult

from webapp.data.requesting.csv_requester import CSVRequester
from webapp.data.transformation.csv_date_transformer import CSVDateTransformer
from webapp.loggers.loggers import build_logger
from webapp.services.dates_service import DatesService


class Covid19DateDataRTL:
    """
    Facade class that abstracts away all the logic for requesting, transforming,
    and loading new CSV date data into MongoDB.
    """
    logger = build_logger("Covid19DateDataRTL")
    dates_service = DatesService()
    csv_requester = CSVRequester()
    csv_date_transformer = CSVDateTransformer()

    def execute_rtl(self) -> str:
        """
        Entry point for the class.
        """
        urls_and_dates = self.csv_requester.check_for_new_csv()

        date_documents = []
        for url, file in urls_and_dates:
            requested_data = self._request(url, file)
            if requested_data:
                date_documents.extend(self._transform(requested_data))

        if not date_documents:
            self.logger.info("No new data!")
            return "No new data!"

        dates = [d["date"].strftime("%d-%m-%Y") for d in date_documents]
        self.logger.info("Loading new transformed data.")
        result = self._load(date_documents)
        if result and result.acknowledged:
            return "Data updated for " + str(dates)

    def _request(self, url: str, filename: str) -> Dict:
        """
        Requests new CSV data from github, should there be any.

        :return:
        """
        return self.csv_requester.request_new_csv(url, filename)

    def _transform(self, data: dict):
        """
        Transforms new CSV data into structure suitable for MongoDB.
        """
        transformed_data = self.csv_date_transformer.transform_csv_data(data)
        if transformed_data:
            return transformed_data

    def _load(self, date_documents: list) -> InsertManyResult:
        """
        Persists new date data as MongoDB documents in covid-19 db.
        """
        return self.dates_service.insert_multiple_dates(date_documents)
