"""
Contains a class that acts as an abstraction layer in front of all the extract,
transform and load logic. CSV data is requested from github, transformed into
objects organised by date and loaded into mongoDB.
"""

from webapp.etl.csv_date_transformer import CSVDateTransformer
from webapp.etl.csv_requester import CSVRequester
from webapp.etl.mongo_dao import MongoDAO


class Covid19DateDataETL:
    """
    todo
    """
    date_documents = []
    dao = MongoDAO("dates")
    csv_requester = CSVRequester()
    csv_date_transformer = CSVDateTransformer()

    def execute_etl(self):
        """
        todo
        """
        urls_and_dates = self.csv_requester.check_for_new_csv()

        if not urls_and_dates:
            print("No new data available!")

        for url, file in urls_and_dates:
            requested_data = self._request(url, file)
            self._transform(requested_data)

        self._load()

    def _request(self, url: str, filename: str):
        """
        todo
        :return:
        """
        return self.csv_requester.request_new_csv(url, filename)

    def _transform(self, data):
        """
        todo
        :return:
        """
        transformed_data = self.csv_date_transformer.transform_csv_data(data)
        if transformed_data:
            self.date_documents.extend(transformed_data)

    def _load(self):
        """
        todo
        :return:
        """
        self.dao.insert_many_documents(self.date_documents)
