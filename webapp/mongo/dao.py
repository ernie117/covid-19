import datetime

from pymongo import MongoClient


entry = {
    "date": datetime.datetime.now().strftime("%m-%d-%Y"),
    "country": "UK",
    "regions/states": [
        {
            "United Kingdom": {
                "confirmed": 1140,
                "deaths": 21,
                "recovered": 18,
                "last update": "2020-03-14T14:53:04"
            },
        },
        {
            "Channel Islands": {
                "confirmed": 2,
                "deaths": 0,
                "recovered": 0,
                "last update": "2020-03-11T20:53:02"
            }
        },
        {
            "Gibraltar": {
                "confirmed": 1,
                "deaths": 0,
                "recovered": 1,
                "last update": datetime.datetime.strptime("2020-03-14T16:33:03",
                                                          "%Y-%m-%dT%H:%M:%S")
            }
        }
    ]
}

client = MongoClient()

db = client.get_database("covid-19")

collection = db.get_collection("dates")

collection.insert_one(entry)
