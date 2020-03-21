"""
todo
"""
import datetime
from typing import Dict

from pymongo import MongoClient


class MongoDAO:
    """
    todo
    """
    client = MongoClient()
    db = client.get_database("covid-19")

    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    def insert_one_document(self, document: Dict):
        """
        todo
        :param document:
        :return:
        """
        collection = self.db.get_collection(self.collection_name)
        collection.insert_one(document)

    def insert_many_documents(self, documents: list):
        """
        todo
        :param documents:
        :return:
        """
        if not documents:
            print("No Documents to insert!")
            return

        collection = self.db.get_collection(self.collection_name)
        collection.insert_many(documents)

    def get_one_document_by_date(self, date: str):
        """
        todo
        :param date:
        :return:
        """
        collection = self.db.get_collection(self.collection_name)
        date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
        return collection.find_one({"date": {"$eq": date_obj}}, {"_id": False})

    def get_many_document_by_date(self, date: str):
        """
        todo
        :param date:
        :return:
        """
        pass
