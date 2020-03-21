"""
Here we'll transform the data retrieved by the request module.
"""

from webapp.mongo.csv_requester import CSVRequester
from webapp.mongo.csv_transformer import CSVTransformer
from webapp.mongo.dao import MongoDAO


class Covid19DateDataETL:
    """
    todo
    """
    new_dates = []
    dao = MongoDAO("dates")
    csv_requester = CSVRequester()

    def extract(self):
        """
        todo
        :return:
        """
        r = self.csv_requester.check_for_new_csv()
        for date, dictreader in r.items():
            transformer = CSVTransformer(date, dictreader)
            self.new_dates.append(transformer.transform_csv_data())

    def persist(self):
        self.dao.insert_many_documents(self.new_dates)
