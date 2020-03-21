"""
Contains a class that acts as an abstraction layer in front of all the extract,
transform and load logic. CSV data is requested from github, transformed into
objects organised by date and loaded into mongoDB.
"""
import json

from webapp.etl.csv_date_transformer import CSVDateTransformer
from webapp.etl.csv_requester import CSVRequester
from webapp.etl.dao import MongoDAO


class Covid19DateDataETL:
    """
    todo
    """
    data = {}
    dates = []
    dao = MongoDAO("dates")
    csv_requester = CSVRequester()
    csv_date_transformer = CSVDateTransformer()

    def execute_etl(self):
        """
        todo
        :return:
        """
        self._extract()
        self._transform()
        # self._load()

    def _extract(self):
        """
        todo
        :return:
        """
        self.data = self.csv_requester.check_for_new_csv()

    def _transform(self):
        """
        todo
        :return:
        """
        self.dates.append(
            self.csv_date_transformer.transform_csv_data(self.data)
        )
        print(json.dumps(self.dates[-1], indent=2, default=str))

    def _load(self):
        """
        todo
        :return:
        """
        self.dao.insert_many_documents(self.dates)
