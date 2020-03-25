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
    date_documents = []
    dates_service = DatesService()
    csv_requester = CSVRequester()
    csv_date_transformer = CSVDateTransformer()

    def execute_rtl(self) -> str:
        """
        Entry point for the class.
        """
        urls_and_dates = self.csv_requester.check_for_new_csv()

        if not urls_and_dates:
            self.logger.info("No new data available!")

        for url, file in urls_and_dates:
            requested_data = self._request(url, file)
            self._transform(requested_data)

        self.logger.info("Loading new transformed data.")
        result = self._load()
        if result and result.acknowledged:
            return "Data updated!"

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
            self.date_documents.extend(transformed_data)

    def _load(self) -> InsertManyResult:
        """
        Persists new date data as MongoDB documents in covid-19 db.
        """
        return self.dates_service.insert_multiple_dates(self.date_documents)
