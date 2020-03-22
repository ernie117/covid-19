"""
todo
"""
import datetime
from typing import Dict, List

from pymongo import MongoClient

from webapp.loggers.loggers import build_logger


class MongoDAO:
    """
    todo
    """
    client = MongoClient()
    db = client.get_database("covid-19")

    def __init__(self, collection_name: str):
        self.logger = build_logger("MongoDAO")
        self.collection_name = collection_name

    def insert_one_document(self, document: Dict) -> None:
        """
        todo
        :param document:
        :return:
        """
        collection = self.db.get_collection(self.collection_name)
        collection.insert_one(document)

    def insert_many_documents(self, documents: List[Dict]) -> None:
        """
        todo
        :param documents:
        :return:
        """
        if not documents:
            self.logger.info("No Documents to insert!")
            return

        collection = self.db.get_collection(self.collection_name)
        self.logger.info("Inserting documents into %s collection",
                         self.collection_name)
        collection.insert_many(documents)

    def get_one_document_by_date(self, date: str) -> Dict:
        """
        todo
        :param date:
        :return:
        """
        collection = self.db.get_collection(self.collection_name)
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        self.logger.info("Retrieving documents by date %s.", date)
        result = collection.find_one({"date": {"$eq": date_obj}}, {"_id": False})

        return result if result else {"not found": "no data for that date"}

    def get_all_dates_by_country(self, country: str) -> List:
        """
        todo
        :return:
        """
        # filter by country and return the confirmed, recovered and deaths
        pipeline = [
            {'$match': {'countries.country/region': country}},
            {'$project': {
                'cases': {'$filter': {
                    'input': '$countries',
                    'as': 'country',
                    'cond': {'$eq': ['$$country.country/region', country]}
                }
                },
                '_id': 0}}
        ]

        collection = self.db.get_collection("dates")
        return sorted(list(collection.aggregate(pipeline)),
                      key=lambda d: d["cases"][0]["confirmed"])
