"""
todo
"""
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
        result = collection.insert_one(document)
        print(result.inserted_id)

    def insert_many_documents(self, documents: list):
        """
        todo
        :param documents:
        :return:
        """
        collection = self.db.get_collection(self.collection_name)
        result = collection.insert_many(documents)
        print(result.inserted_ids)

    def get_one_document_by_date(self, date: str):
        """
        todo
        :param date:
        :return:
        """
        pass

    def get_many_document_by_date(self, date: str):
        """
        todo
        :param date:
        :return:
        """
        pass
