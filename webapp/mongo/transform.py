"""
Here we'll transform the data retrieved by the request module.
"""
import json

from webapp.mongo.csv_requester import CSVRequester
from webapp.mongo.csv_transformer import CSVTransformer


class Transformer:
    """
    todo
    """

    def __init__(self):
        self.csv_requester = CSVRequester()

    def main(self):
        """
        todo
        :return:
        """
        r = self.csv_requester.check_for_new_csv()
        for date, dictreader in r.items():
            transformer = CSVTransformer(date, dictreader)
            stuff = transformer.transform_csv_data()
            print(json.dumps(stuff, indent=2))
