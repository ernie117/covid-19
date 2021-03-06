"""
Contains the class acting as the direct interface to a standalone MongoDB
'covid-19'.
"""
import datetime
from typing import Dict, List

from flask import current_app
from pymongo import MongoClient, WriteConcern
from pymongo.command_cursor import CommandCursor
from pymongo.cursor import Cursor
from pymongo.results import InsertManyResult, InsertOneResult

from webapp.utils.loggers import build_logger

LOGGER = build_logger("MongoDAO")


class MongoDAO:
    """
    Data access class that uses the PyMongo package to interact directly with
    a standalone mongo instance to retrieve and insert documents to and from the
    'covid-19' db.
    """

    client = MongoClient(
        username=current_app.config["MONGO_USERNAME"],
        password=current_app.config["MONGO_PASSWORD"],
    )
    db = client.get_database("covid-19")

    def __init__(self, collection_name: str):
        self.collection_name = collection_name
        self.collection = self.db.get_collection(
            collection_name, write_concern=WriteConcern(w=1)
        )

    def insert_one_document(self, document: Dict) -> InsertOneResult:
        """
        Insert a single document into specified collection of covid-19 db.

        :param document: Dict representing document to be persisted.
        :return: InsertOneResult representing our write result.
        """
        LOGGER.info("Inserting one document in %s.", self.collection_name)

        return self.collection.insert_one(document)

    def insert_many_documents(self, documents: List[Dict]) -> InsertManyResult:
        """
        Inserts multiple documents into the specified collection of covid-19 db.

        :param documents: Multiple dicts representing documents to be persisted.
        :return: InsertManyResult representing our write result.
        """
        LOGGER.info(
            "Inserting %d documents into %s collection",
            len(documents),
            self.collection_name,
        )

        return self.collection.insert_many(documents)

    def get_one_document_by_date(self, date: datetime) -> Dict:
        """
        Retrieves one document from the specified collection of covid-19 db
        by date key.

        :param date: Datetime object representing date to query by.
        :return: Dict representing document matching date, if any.
        """
        LOGGER.info("Retrieving documents by date %s.", date)

        return self.collection.find_one({"date": {"$eq": date}}, {"_id": False})

    def get_all_dates_by_country(self, country: str) -> CommandCursor:
        """
        Retrieves multiple documents from the specified collection of covid-19 db
        by country.

        :return: CommandCursor iterator of matching documents.
        """
        LOGGER.info("Retrieving multiple dates for %s by aggregate.", country)
        pipeline = [
            {
                "$project": {
                    "cases": {
                        "$filter": {
                            "input": "$countries",
                            "as": "cases",
                            "cond": {"$eq": ["$$cases.country/region", country]},
                        }
                    },
                    "date": 1,
                    "_id": 0,
                }
            }
        ]

        return self.collection.aggregate(pipeline=pipeline)

    def get_all(self) -> Cursor:
        """
        Sometimes you just need everything.

        :return: Iterator over all documents.
        """
        return self.collection.find()
