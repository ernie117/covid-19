"""
Contains a class that acts as an abstraction layer in front
of all the extract, transform and load logic. CSV data is
requested from github, transformed by CSVTransformer and
loaded into mongoDB.
"""

from webapp.mongo.csv_requester import CSVRequester
from webapp.mongo.csv_transformer import CSVTransformer
from webapp.mongo.dao import MongoDAO


class Covid19DateDataETL:
    """
    todo
    """
    data = {}
    dates = []
    dao = MongoDAO("dates")
    csv_requester = CSVRequester()

    def execute_etl(self):
        """
        todo
        :return:
        """
        self._extract()
        self._transform()
        self._load()

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
        for date, dictreader in self.data.items():
            transformer = CSVTransformer(date, dictreader)
            self.dates.append(transformer.transform_csv_data())

    def _load(self):
        """
        todo
        :return:
        """
        self.dao.insert_many_documents(self.dates)
