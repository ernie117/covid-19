import datetime
from typing import Dict

from pymongo import MongoClient


###### example document format to follow ######
# entry = {
#     "date": datetime.datetime.now().strftime("%m-%d-%Y"),
#     "country": "UK",
#     "regions/states": [
#         {
#             "United Kingdom": {
#                 "confirmed": 1140,
#                 "deaths": 21,
#                 "recovered": 18,
#                 "last update": "2020-03-14T14:53:04"
#             },
#         },
#         {
#             "Channel Islands": {
#                 "confirmed": 2,
#                 "deaths": 0,
#                 "recovered": 0,
#                 "last update": "2020-03-11T20:53:02"
#             }
#         },
#         {
#             "Gibraltar": {
#                 "confirmed": 1,
#                 "deaths": 0,
#                 "recovered": 1,
#                 "last update": datetime.datetime.strptime("2020-03-14T16:33:03",
#                                                           "%Y-%m-%dT%H:%M:%S")
#             }
#         }
#     ]
# }


CLIENT = MongoClient()
COVID_DB = CLIENT.get_database("covid-19")


def insert_one_document(document: Dict, collection_name: str):
    collection = COVID_DB.get_collection(collection_name)
    result = collection.insert_one(document)
    print(result.inserted_id)


def insert_many_documents(documents: list, collection_name: str):
    collection = COVID_DB.get_collection(collection_name)
    result = collection.insert_many(documents)
    print(result.inserted_ids)
